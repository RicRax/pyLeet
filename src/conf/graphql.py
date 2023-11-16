from . import config

leetCodeUrl = "https://leetcode.com/graphql"

randomQuestionQuery = """query questionContent($titleSlug: String!) {
  question(titleSlug: $titleSlug) {
    content
    titleSlug
  }
}"""


cookies = {"LEETCODE_SESSION": config.leetCodeSession, "csrftoken": config.csrfToken}

headers = {
    "Content-Type": "application/json",
    "x-csrftoken": config.csrfToken,
    "Origin": "https://leetcode.com",
    "Referer": "https://leetcode.com",
    "Connection": "keep-alive",
}

headersSubmit = {
    "content-Type": "application/json",
    "x-csrftoken": config.csrfToken,
    "Origin": "https://leetcode.com",
    "Referer": "https://leetcode.com/problems/two-sum/",
}

problemSetQuery = """
query problemsetQuestionList($categorySlug: String, $limit: Int, $skip: Int, $filters: QuestionListFilterInput) {
    problemsetQuestionList: questionList(
        categorySlug: $categorySlug
        limit: $limit
        skip: $skip
        filters: $filters
    ) {
        total: totalNum
        questions: data {
            acRate
            difficulty
            freqBar
            frontendQuestionId: questionFrontendId
            isFavor
            paidOnly: isPaidOnly
            status
            title
            titleSlug
            topicTags {
                name
                id
                slug
            }
            hasSolution
            hasVideoSolution
        }
    }
}


"""
