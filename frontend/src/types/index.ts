export interface AgentStatus {
  agent_name: string
  status: 'pending' | 'running' | 'completed' | 'error'
  started_at: string
  completed_at: string
}

export interface SkillLevel {
  skill: string
  level: number
}

export interface SkillGap {
  skill: string
  current_level: number
  target_level: number
  gap: number
  priority: 'high' | 'medium' | 'low'
}

export interface CourseResource {
  course_id: string
  title: string
  platform: string
  url: string
  duration_hours: number
  cost_eur: number
  rating: number
  skill_tags: string[]
}

export interface TrainingModule {
  module_id: string
  title: string
  description: string
  skill_area: 'hard' | 'soft'
  topics: string[]
  courses: CourseResource[]
  duration_weeks: number
  milestone: string
}

export interface MentorMatch {
  mentor_id: string
  name: string
  role: string
  expertise: string[]
  match_score: number
  rationale: string
  availability: string
}

export interface CostBreakdown {
  total_course_cost_eur: number
  total_hours: number
  estimated_duration_weeks: number
  roi_estimate: string
  cost_per_module: {
    module_id: string
    module_title: string
    cost_eur: number
    hours: number
    duration_weeks: number
    num_courses: number
  }[]
}

export interface AssessmentQuestion {
  question_id: string
  category: 'technical' | 'situational' | 'interest'
  skill_area: string
  question_text: string
  question_type: 'multiple_choice' | 'scale' | 'open'
  options: string[]
}

export interface YouTubeVideo {
  video_id: string
  title: string
  url: string
  channel: string
  duration_minutes: number
  relevance_note: string
}

export interface QuizQuestion {
  quiz_id: string
  question_text: string
  options: string[]
  correct_answer: number
  explanation: string
}

export interface LessonContent {
  lesson_id: string
  title: string
  content_markdown: string
  youtube_videos: YouTubeVideo[]
  quiz: QuizQuestion[]
}

export interface CustomCourse {
  custom_course_id: string
  module_id: string
  title: string
  skill_area: string
  description: string
  lessons: LessonContent[]
  estimated_hours: number
}

export interface ReviewFeedback {
  status: 'approved' | 'changes_requested'
  comments: string
  requested_changes: string[]
}

export interface PlanStatus {
  request_id: string
  employee_id: string
  employee_name: string | null
  target_position: string
  current_phase: string
  agent_statuses: AgentStatus[]
  hard_skills: SkillLevel[] | null
  soft_skills: SkillLevel[] | null
  experience_summary: string | null
  current_role: string | null
  assessment_questions: AssessmentQuestion[] | null
  assessment_completed: boolean | null
  skill_gaps: SkillGap[] | null
  training_plan: TrainingModule[] | null
  plan_summary: string | null
  cost_breakdown: CostBreakdown | null
  assigned_mentor: MentorMatch | null
  custom_courses: CustomCourse[] | null
  review_status: string | null
  review_feedback: ReviewFeedback | null
}

export interface RequestSummary {
  request_id: string
  employee_id: string
  employee_name: string
  target_position: string
  current_phase: string
  requester_type: string
  review_status: string
}
