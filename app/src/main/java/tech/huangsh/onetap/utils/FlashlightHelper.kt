package tech.huangsh.onetap.utils

import android.content.Context
import android.hardware.camera2.CameraCharacteristics
import android.hardware.camera2.CameraManager
import android.util.Log

/**
 * 手电筒助手
 * 用于全局控制手电筒状态
 */
object FlashlightHelper {
    private const val TAG = "FlashlightHelper"
    private var isFlashlightOn = false

    /**
     * 切换手电筒状态
     */
    fun toggle(context: Context): Boolean {
        return if (isFlashlightOn) {
            turnOff(context)
        } else {
            turnOn(context)
        }
    }

    /**
     * 打开手电筒
     */
    fun turnOn(context: Context): Boolean {
        return try {
            val cameraManager = context.getSystemService(Context.CAMERA_SERVICE) as CameraManager
            val cameraId = findFlashCameraId(cameraManager)
            if (cameraId != null) {
                cameraManager.setTorchMode(cameraId, true)
                isFlashlightOn = true
                true
            } else {
                Log.w(TAG, "未发现带闪光灯的摄像头")
                false
            }
        } catch (e: Exception) {
            Log.e(TAG, "打开手电筒失败", e)
            false
        }
    }

    /**
     * 关闭手电筒
     */
    fun turnOff(context: Context): Boolean {
        return try {
            val cameraManager = context.getSystemService(Context.CAMERA_SERVICE) as CameraManager
            val cameraId = findFlashCameraId(cameraManager)
            if (cameraId != null) {
                cameraManager.setTorchMode(cameraId, false)
                isFlashlightOn = false
                true
            } else {
                false
            }
        } catch (e: Exception) {
            Log.e(TAG, "关闭手电筒失败", e)
            false
        }
    }

    /**
     * 获取当前状态
     */
    fun isOn(): Boolean = isFlashlightOn

    /**
     * 查找支持闪光灯的摄像头ID
     */
    private fun findFlashCameraId(cameraManager: CameraManager): String? {
        return try {
            cameraManager.cameraIdList.firstOrNull { id ->
                cameraManager.getCameraCharacteristics(id)
                    .get(CameraCharacteristics.FLASH_INFO_AVAILABLE) == true
            }
        } catch (e: Exception) {
            null
        }
    }
}
