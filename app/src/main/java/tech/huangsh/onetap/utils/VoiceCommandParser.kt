package tech.huangsh.onetap.utils

/**
 * 语音指令解析器
 * 
 * 从语音识别输出的文字中提取用户意图(Action)和目标参数(targetName)。
 * 采用"关键词匹配 + 编辑距离容错"策略。
 */
object VoiceCommandParser {

    /**
     * 支持的动作类型（可扩展）
     */
    enum class Action {
        CALL,           // 打电话
        OPEN_APP,       // 打开应用 (预留)
        FLASHLIGHT,     // 开/关手电筒 (预留)
        UNKNOWN         // 未识别
    }

    /**
     * 解析结果
     */
    data class VoiceCommand(
        val action: Action,
        val targetName: String
    )

    /**
     * 每种动作对应的关键词库
     */
    private val actionKeywords: Map<Action, List<String>> = mapOf(
        Action.CALL to listOf(
            "打电话", "拨打", "呼叫", "通话", "联系",
            "拨给", "打给", "电话", "拨号", "打个电话"
        ),
        Action.OPEN_APP to listOf(
            "打开", "启动", "运行", "开启", "用一下"
        ),
        Action.FLASHLIGHT to listOf(
            "手电筒", "手电", "照明", "照亮"
        )
    )

    /**
     * 需要从目标文字中清除的连接词/助词
     */
    private val stopWords = listOf(
        "给", "的", "跟", "和", "帮我", "帮忙", "请",
        "一下", "吧", "呢", "啊", "吗", "了",
        "我要", "我想", "帮我给"
    )

    /**
     * 主入口：从原始STT文字中解析出 VoiceCommand
     */
    fun parseCommand(text: String): VoiceCommand? {
        if (text.isBlank()) return null

        val cleanText = text.trim()
        android.util.Log.d("VoiceCommandParser", "开始解析指令: $cleanText")

        // 尝试匹配每种动作
        for ((action, keywords) in actionKeywords) {
            val matchedKeyword = findMatchingKeyword(cleanText, keywords)
            if (matchedKeyword != null) {
                // 提取目标名称
                val targetName = extractTargetName(cleanText, matchedKeyword)
                android.util.Log.d("VoiceCommandParser", "解析成功: action=$action, target=$targetName")
                return VoiceCommand(action = action, targetName = targetName)
            }
        }

        android.util.Log.w("VoiceCommandParser", "无法识别指令意图: $cleanText")
        return null
    }

    /**
     * 在文本中查找匹配的关键词（精确 + 编辑距离容错）
     */
    private fun findMatchingKeyword(text: String, keywords: List<String>): String? {
        // 第一优先级：精确包含
        for (keyword in keywords) {
            if (text.contains(keyword)) {
                return keyword
            }
        }

        // 第二优先级：编辑距离容错（针对 ≥ 2 字的关键词）
        for (keyword in keywords) {
            if (keyword.length < 2) continue
            // 对文本中每个和关键词等长的连续子串计算编辑距离
            val len = keyword.length
            for (i in 0..text.length - len) {
                val substr = text.substring(i, i + len)
                if (editDistance(substr, keyword) <= 1) {
                    return keyword
                }
            }
        }

        return null
    }

    /**
     * 提取目标名称：去掉动作关键词和停用词，剩余的就是目标
     */
    private fun extractTargetName(text: String, matchedKeyword: String): String {
        var result = text

        // 移除匹配到的关键词
        result = result.replace(matchedKeyword, "")

        // 移除停用词
        for (stopWord in stopWords) {
            result = result.replace(stopWord, "")
        }

        // 清理空白
        return result.trim()
    }

    /**
     * 计算两个字符串之间的编辑距离 (Levenshtein Distance)
     */
    fun editDistance(a: String, b: String): Int {
        val m = a.length
        val n = b.length
        val dp = Array(m + 1) { IntArray(n + 1) }

        for (i in 0..m) dp[i][0] = i
        for (j in 0..n) dp[0][j] = j

        for (i in 1..m) {
            for (j in 1..n) {
                val cost = if (a[i - 1] == b[j - 1]) 0 else 1
                dp[i][j] = minOf(
                    dp[i - 1][j] + 1,       // 删除
                    dp[i][j - 1] + 1,        // 插入
                    dp[i - 1][j - 1] + cost  // 替换
                )
            }
        }
        return dp[m][n]
    }
}
