package tech.huangsh.onetap.utils

import tech.huangsh.onetap.data.model.Contact

/**
 * 联系人模糊匹配器
 * 
 * 从联系人列表中根据语音识别出的名称进行模糊匹配，
 * 采用 精确 → 包含 → 拼音 → 编辑距离 四层匹配策略。
 */
object ContactMatcher {
    private const val TAG = "ContactMatcher"

    /**
     * 匹配结果
     */
    data class MatchResult(
        val contact: Contact,
        val confidence: Float  // 0.0 ~ 1.0，越高越可信
    )

    /**
     * 从联系人列表中找到与 targetName 最匹配的联系人
     * @param targetName 语音解析出的目标名
     * @param contacts 完整的联系人列表
     * @return 最佳匹配结果，没有足够信心的匹配则返回 null
     */
    fun findBestMatch(targetName: String, contacts: List<Contact>): MatchResult? {
        if (targetName.isBlank() || contacts.isEmpty()) return null

        val candidates = mutableListOf<MatchResult>()

        for (contact in contacts) {
            val score = calculateMatchScore(targetName, contact.name)
            if (score > 0f) {
                candidates.add(MatchResult(contact, score))
            }
        }

        // 按置信度降序，返回最优结果
        val best = candidates.maxByOrNull { it.confidence }

        // 置信度至少 0.3 才认为是有效匹配
        return if (best != null && best.confidence >= 0.3f) best else null
    }

    /**
     * 计算目标名与联系人名的匹配分数
     */
    private fun calculateMatchScore(targetName: String, contactName: String): Float {
        val target = targetName.trim()
        val name = contactName.trim()

        // 第一优先级：完全相等 → 1.0
        if (target == name) return 1.0f

        // 第二优先级：包含关系 → 0.8
        if (name.contains(target) || target.contains(name)) return 0.8f

        // 第三优先级：拼音首字母完全匹配 → 0.7
        val targetPinyin = toPinyinInitials(target)
        val namePinyin = toPinyinInitials(name)
        if (targetPinyin.isNotEmpty() && targetPinyin == namePinyin) return 0.7f

        // 第四优先级：编辑距离容错
        val distance = VoiceCommandParser.editDistance(target, name)
        // 对于短名字 (≤3字)，编辑距离为1就认为匹配
        // 对于长名字，按比例阈值
        val maxLen = maxOf(target.length, name.length)
        val threshold = if (maxLen <= 3) 1 else (maxLen * 0.4).toInt()
        if (distance <= threshold) {
            // 距离越小分数越高
            return (0.6f * (1f - distance.toFloat() / maxLen.toFloat()))
        }

        // 第五优先级：拼音首字母编辑距离 → 0.4
        if (targetPinyin.isNotEmpty() && namePinyin.isNotEmpty()) {
            val pinyinDistance = VoiceCommandParser.editDistance(targetPinyin, namePinyin)
            if (pinyinDistance <= 1) return 0.4f
        }

        return 0f
    }

    /**
     * 将中文字符串转换为拼音首字母（简易版）
     * 利用 ChineseUtils 现有的 getFirstLetter 方法
     */
    private fun toPinyinInitials(text: String): String {
        return text.map { char ->
            if (ChineseUtils.isChinese(char)) {
                ChineseUtils.getFirstLetter(char.toString())
            } else {
                char.uppercaseChar().toString()
            }
        }.joinToString("")
    }
}
