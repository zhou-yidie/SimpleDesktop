package tech.huangsh.onetap.plugin.impl

import android.content.Context
import android.content.Intent
import androidx.compose.runtime.Composable
import androidx.compose.ui.platform.LocalContext
import dagger.hilt.android.qualifiers.ApplicationContext
import kotlinx.coroutines.flow.first
import kotlinx.coroutines.launch
import tech.huangsh.onetap.data.model.Contact
import tech.huangsh.onetap.data.repository.ContactRepository
import tech.huangsh.onetap.plugin.*
import tech.huangsh.onetap.ui.screens.contact.ContactDetailScreen
import tech.huangsh.onetap.ui.screens.contact.ContactManagementScreen
import tech.huangsh.onetap.viewmodel.ContactViewModel
import javax.inject.Inject
import javax.inject.Singleton

/**
 * 联系人插件
 * 提供联系人管理功能
 */
@Singleton
class ContactPlugin @Inject constructor(
    @ApplicationContext private val appContext: Context,
    private val contactRepository: ContactRepository
) : BasePlugin(), IPluginEventListener {
    
    // 联系人ViewModel（在实际应用中应该通过依赖注入获取）
    private var contactViewModel: ContactViewModel? = null
    
    override val pluginId: String = "contact_plugin"
    override val name: String = "联系人管理"
    override val version: String = "1.0.0"
    override val description: String = "提供联系人管理功能，包括添加、编辑、删除联系人，以及拨打电话和微信通话"
    override val author: String = "SimpleDesktop Team"
    
    override suspend fun onInitializing() {
        super.onInitializing()
        
        // 初始化插件配置
        val config = getConfigStorage()
        if (!config.contains("initialized")) {
            // 设置默认配置
            config.setValue("max_contacts", 50)
            config.setValue("enable_wechat_integration", true)
            config.setValue("enable_phone_call", true)
            config.setValue("initialized", true)
        }
    }
    
    override suspend fun onStarted() {
        super.onStarted()
        
        // 注册消息处理器
        registerMessageHandler("get_contacts") { message ->
            handleGetContacts(message)
        }
        
        registerMessageHandler("add_contact") { message ->
            handleAddContact(message)
        }
        
        registerMessageHandler("update_contact") { message ->
            handleUpdateContact(message)
        }
        
        registerMessageHandler("delete_contact") { message ->
            handleDeleteContact(message)
        }
        
        registerMessageHandler("make_phone_call") { message ->
            handleMakePhoneCall(message)
        }
        
        registerMessageHandler("make_wechat_call") { message ->
            handleMakeWeChatCall(message)
        }
        
        registerMessageHandler("get_contact_ui") { message ->
            handleGetContactUI(message)
        }
    }
    
    override fun getMainComponent(): Any? {
        return ContactManagementScreenRoute
    }
    
    override fun getConfigScreen(): Any? {
        return ContactPluginConfigScreen
    }
    
    override suspend fun onPluginEvent(event: PluginEvent) {
        when (event) {
            is PluginEvent.AppStarted -> {
                // 应用启动时，可以执行一些初始化逻辑
                val config = getConfigStorage()
                val enableWeChatIntegration = config.getBoolean("enable_wechat_integration", true)
                
                if (enableWeChatIntegration) {
                    // 检查微信是否安装
                    checkWeChatInstallation()
                }
            }
            else -> {
                // 其他事件处理
            }
        }
    }
    
    /**
     * 处理获取联系人列表的请求
     */
    private suspend fun handleGetContacts(message: PluginMessage): PluginMessage {
        return try {
            val contacts = contactRepository.allContacts.first()
            val contactsJson = contacts.map { contact ->
                mapOf(
                    "id" to contact.id.toString(),
                    "name" to contact.name,
                    "phone" to (contact.phone ?: ""),
                    "wechatNickname" to (contact.wechatNickname ?: ""),
                    "avatarUri" to (contact.avatarUri ?: ""),
                    "hasVideoCall" to contact.hasVideoCall,
                    "hasVoiceCall" to contact.hasVoiceCall,
                    "hasPhoneCall" to contact.hasPhoneCall
                )
            }
            
            PluginMessage.createResponse(
                message,
                mapOf(
                    "contacts" to contactsJson.toString(),
                    "count" to contacts.size.toString()
                )
            )
        } catch (e: Exception) {
            e.printStackTrace()
            PluginMessage.createResponse(
                message,
                mapOf("error" to (e.message ?: "Unknown error") as String)
            )
        }
    }
    
    /**
     * 处理添加联系人的请求
     */
    private suspend fun handleAddContact(message: PluginMessage): PluginMessage {
        return try {
            val name = message.data["name"] ?: return PluginMessage.createResponse(
                message,
                mapOf("error" to "Missing name")
            )
            
            val phone = message.data["phone"]
            val wechatNickname = message.data["wechatNickname"]
            val avatarUri = message.data["avatarUri"]
            
            val contact = Contact(
                name = name,
                phone = phone,
                wechatNickname = wechatNickname,
                avatarUri = avatarUri,
                hasPhoneCall = !phone.isNullOrEmpty(),
                hasVideoCall = !wechatNickname.isNullOrEmpty(),
                hasVoiceCall = !wechatNickname.isNullOrEmpty()
            )
            
            val id = contactRepository.insertContact(contact)
            
            PluginMessage.createResponse(
                message,
                mapOf(
                    "success" to "true",
                    "id" to id.toString()
                )
            )
        } catch (e: Exception) {
            e.printStackTrace()
            PluginMessage.createResponse(
                message,
                mapOf("error" to (e.message ?: "Unknown error") as String)
            )
        }
    }
    
    /**
     * 处理更新联系人的请求
     */
    private suspend fun handleUpdateContact(message: PluginMessage): PluginMessage {
        return try {
            val id = message.data["id"]?.toLongOrNull() ?: return PluginMessage.createResponse(
                message,
                mapOf("error" to "Invalid id")
            )
            
            val contact = contactRepository.getContactById(id) ?: return PluginMessage.createResponse(
                message,
                mapOf("error" to "Contact not found")
            )
            
            val name = message.data["name"] ?: contact.name
            val phone = message.data["phone"]
            val wechatNickname = message.data["wechatNickname"]
            val avatarUri = message.data["avatarUri"]
            val hasVideoCall = message.data["hasVideoCall"]?.toBoolean() ?: contact.hasVideoCall
            val hasVoiceCall = message.data["hasVoiceCall"]?.toBoolean() ?: contact.hasVoiceCall
            val hasPhoneCall = message.data["hasPhoneCall"]?.toBoolean() ?: contact.hasPhoneCall
            
            val updatedContact = contact.copy(
                name = name,
                phone = phone,
                wechatNickname = wechatNickname,
                avatarUri = avatarUri,
                hasVideoCall = hasVideoCall,
                hasVoiceCall = hasVoiceCall,
                hasPhoneCall = hasPhoneCall
            )
            
            contactRepository.updateContact(updatedContact)
            
            PluginMessage.createResponse(
                message,
                mapOf("success" to "true")
            )
        } catch (e: Exception) {
            e.printStackTrace()
            PluginMessage.createResponse(
                message,
                mapOf("error" to (e.message ?: "Unknown error") as String)
            )
        }
    }
    
    /**
     * 处理删除联系人的请求
     */
    private suspend fun handleDeleteContact(message: PluginMessage): PluginMessage {
        return try {
            val id = message.data["id"]?.toLongOrNull() ?: return PluginMessage.createResponse(
                message,
                mapOf("error" to "Invalid id")
            )
            
            contactRepository.deleteContactById(id.toInt())
            
            PluginMessage.createResponse(
                message,
                mapOf("success" to "true")
            )
        } catch (e: Exception) {
            e.printStackTrace()
            PluginMessage.createResponse(
                message,
                mapOf("error" to (e.message ?: "Unknown error") as String)
            )
        }
    }
    
    /**
     * 处理拨打电话的请求
     */
    private suspend fun handleMakePhoneCall(message: PluginMessage): PluginMessage {
        return try {
            val phoneNumber = message.data["phoneNumber"] ?: return PluginMessage.createResponse(
                message,
                mapOf("error" to "Missing phone number")
            )
            
            val intent = contactRepository.makePhoneCall(phoneNumber)
            if (intent != null) {
                context.startActivity(intent)
                PluginMessage.createResponse(
                    message,
                    mapOf("success" to "true")
                )
            } else {
                PluginMessage.createResponse(
                    message,
                    mapOf("error" to "Failed to create call intent")
                )
            }
        } catch (e: Exception) {
            e.printStackTrace()
            PluginMessage.createResponse(
                message,
                mapOf("error" to (e.message ?: "Unknown error") as String)
            )
        }
    }
    
    /**
     * 处理微信通话的请求
     */
    private suspend fun handleMakeWeChatCall(message: PluginMessage): PluginMessage {
        return try {
            val wechatNickname = message.data["wechatNickname"] ?: return PluginMessage.createResponse(
                message,
                mapOf("error" to "Missing WeChat nickname")
            )
            
            val isVideo = message.data["isVideo"]?.toBoolean() ?: true
            
            val success = if (isVideo) {
                contactRepository.startWeChatVideoCall(wechatNickname)
            } else {
                contactRepository.startWeChatVoiceCall(wechatNickname)
            }
            
            PluginMessage.createResponse(
                message,
                mapOf("success" to success.toString())
            )
        } catch (e: Exception) {
            e.printStackTrace()
            PluginMessage.createResponse(
                message,
                mapOf("error" to (e.message ?: "Unknown error") as String)
            )
        }
    }
    
    /**
     * 处理获取联系人UI的请求
     */
    private suspend fun handleGetContactUI(message: PluginMessage): PluginMessage {
        return try {
            val screenType = message.data["screenType"] ?: "management"
            
            val uiComponent = when (screenType) {
                "detail" -> "ContactDetailScreen"
                "management" -> "ContactManagementScreen"
                else -> "ContactManagementScreen"
            }
            
            PluginMessage.createResponse(
                message,
                mapOf("uiComponent" to uiComponent)
            )
        } catch (e: Exception) {
            e.printStackTrace()
            PluginMessage.createResponse(
                message,
                mapOf("error" to (e.message ?: "Unknown error") as String)
            )
        }
    }
    
    /**
     * 检查微信是否安装
     */
    private fun checkWeChatInstallation() {
        try {
            context.packageManager.getPackageInfo("com.tencent.mm", 0)
            // 微信已安装
        } catch (e: Exception) {
            // 微信未安装
        }
    }
}

/**
 * 联系人管理屏幕路由
 */
object ContactManagementScreenRoute

/**
 * 联系人详情屏幕路由
 */
object ContactDetailScreenRoute

/**
 * 联系人插件配置屏幕
 */
object ContactPluginConfigScreen

/**
 * 联系人插件UI组件
 */
object ContactPluginUIComponents {
    @Composable
    fun ContactManagementScreenWrapper(
        viewModel: ContactViewModel
    ) {
        ContactManagementScreen(
            onBack = {
                // 处理返回
            },
            onAddContact = {
                // 处理添加联系人
            },
            viewModel = viewModel
        )
    }
    
    @Composable
    fun ContactDetailScreenWrapper(contactId: Long) {
        ContactDetailScreen(
            contact = null, // 需要根据contactId加载联系人
            isEditMode = false,
            onBack = {
                // 处理返回
            },
            onSave = { contact ->
                // 处理保存
            },
            onDelete = { contact ->
                // 处理删除
            },
            onImageSelected = { uri ->
                // 处理图片选择
            }
        )
    }
}