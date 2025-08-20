# [PROJECT NAME] STATE DOCUMENT

# ⚠️ 🚨 CRITICAL UPDATE PROTOCOL - READ BEFORE ANY CHANGES 🚨 ⚠️

## ⛔ UPDATE_PROTOCOL ⛔
**🚨 ENFORCEMENT: MANDATORY - ZERO TOLERANCE FOR VIOLATIONS 🚨**
**⚠️ VIOLATION CONSEQUENCES: Protocol violations break historical continuity and project tracking ⚠️**
**📋 BEFORE ANY EDIT: Read this section completely. Follow format exactly. No exceptions.**

DATETIME_VERIFICATION: Use `ntpdate -q time.nist.gov` or `curl -s http://worldtimeapi.org/api/timezone/UTC` for verified UTC timestamps - NO HALLUCINATIONS ALLOWED
UPDATE_TYPES: STATUS_CHANGE|NEW_COMPONENT|ISSUE_RESOLUTION|ACHIEVEMENT|ARCHITECTURAL_DECISION|TECHNICAL_DEBT
APPEND_FORMAT: Add new entries to appropriate section using same compact syntax
STATUS_UPDATES: Modify existing STATUS field in place, append RESOLUTION or NOTES if needed
ACHIEVEMENT_FORMAT: achievement_YYYY_MM_DD_HH_MM_SS_description { verified_datetime: [system_clock_output]; scope: description; achievement: specific_outcome; impact: measurable_change; files: [modified_files] }
ISSUE_FORMAT: issue_YYYY_MM_DD_HH_MM_SS_description { verified_datetime: [system_clock_output]; issue: specific_problem; impact: effect_on_system; status: current_state; location: [relevant_files]; priority: CRITICAL|HIGH|MEDIUM|LOW }
COMPONENT_UPDATE: Modify existing component entries in place, preserve all existing fields, add new fields with semicolon delimiter
ARCHITECTURAL_DECISION_UPDATE: Add new decision with rationale, implementation details, affected components
**🔒 NO_REMOVAL: NEVER remove historical data - only append or modify status 🔒**
**⏰ VERIFICATION_REQUIRED: Any datetime must be verified with actual system clock before entry ⏰**

**🛑 PROHIBITED ACTIONS:**
- ❌ Replacing entire file content
- ❌ Removing historical entries
- ❌ Changing existing achievement/issue IDs
- ❌ Using fictional timestamps
- ❌ Ignoring the compact syntax format

**✅ REQUIRED ACTIONS:**
- ✅ Read existing content completely before changes
- ✅ Follow APPEND_FORMAT for new entries
- ✅ Preserve all historical data
- ✅ Use exact datetime verification
- ✅ Maintain compact syntax consistency

# 📊 PROJECT DATA BELOW - FOLLOW PROTOCOL ABOVE

## FORMAT_KEY
STATUS: COMPLETE|PARTIAL|BLOCKED|IN_PROGRESS|PLANNED|DEFERRED; PRIORITY: CRITICAL|HIGH|MEDIUM|LOW; CATEGORY: [YOUR_CATEGORIES]; REFS: [file/path] {config_key} <service_name>

## PROJECT_METADATA
PROJECT_ID: [your-project-id]; BUSINESS_MODEL: [your-business-model]; TIMELINE: [project-timeline]; TARGETS: [target-audience]; CURRENT_PHASE: [current-development-phase]; DEV_CADENCE: [development-schedule]

## PHASE_STATUS
PHASE_1 { NAME: [Phase Name]; DURATION: [start-date] → [end-date] ([duration]); STATUS: [COMPLETE|IN_PROGRESS|PLANNED]; SYSTEM: [development-environment]; DELIVERABLES: [key-deliverables] }
PHASE_2 { NAME: [Phase Name]; DURATION: [dates]; STATUS: [status]; DEPS: [dependencies] }
[Continue with additional phases...]

## COMPONENT_STATUS
[CATEGORY]_COMPONENTS { [component_name] { STATUS: [status]; PATTERN: [implementation-pattern]; FILES: [file-references]; COMMANDS: [build-commands] }; [component_name_2] { STATUS: [status]; PURPOSE: [purpose]; DEPS: [dependencies] } }

[Continue with additional component categories...]

## ARCHITECTURAL_DECISIONS
[decision_name] { DECISION: [what-was-decided]; RATIONALE: [why-this-decision]; IMPLEMENTATION: [how-implemented]; STATUS: [COMPLETE|IN_PROGRESS|PLANNED]; FILES: [affected-files] }

[Continue with additional decisions...]

## ACHIEVEMENTS
achievement_YYYY_MM_DD_HH_MM_SS_[description] { verified_datetime: [verified-timestamp]; scope: [scope-of-work]; achievement: [what-was-accomplished]; impact: [measurable-impact]; files: [modified-files] }

[Continue with additional achievements...]

## CURRENT_ISSUES
CRITICAL_ISSUES { [issue_name] { ISSUE: [problem-description]; IMPACT: [effect-on-system]; STATUS: [current-state]; LOCATION: [relevant-files]; PRIORITY: CRITICAL; DETAILS: [additional-context] } }
HIGH_PRIORITY_ISSUES { [issue_name] { ISSUE: [problem]; IMPACT: [impact]; STATUS: [status]; LOCATION: [files]; PRIORITY: HIGH } }
MEDIUM_PRIORITY_ISSUES { [issue_name] { ISSUE: [problem]; IMPACT: [impact]; STATUS: [status]; PRIORITY: MEDIUM } }

## RESOLVED_ISSUES
issue_YYYY_MM_DD_HH_MM_SS_[description] { verified_datetime: [timestamp]; issue: [problem-description]; impact: [system-effect]; status: RESOLVED; location: [files]; resolution: [how-it-was-fixed]; priority: [original-priority] }

[Continue with additional resolved issues...]

## TECHNICAL_DEBT
CRITICAL_DEBT { [debt_item] { ISSUE: [technical-debt-description]; IMPACT: [effect-on-development]; SOLUTION: [proposed-fix]; LOCATIONS: [affected-files] } }
HIGH_PRIORITY_DEBT { [debt_item] { SCOPE: [area-of-debt]; REQUIREMENTS: [what-needs-to-be-done]; LOCATION: [files] } }

[Continue with additional debt categories...]

## DEVELOPMENT_ENVIRONMENT
INFRASTRUCTURE_STATUS { [tool_name]: [version] ([status-notes]); [service_name]: [status] ([description]) }
SERVICE_HEALTH { <[service-name]>: [STATUS] ([description]); [additional-services] }
DEVELOPMENT_COMMANDS { [command_category]: [command] ([description]); [build_targets]: [make-commands] }

## CRITICAL_PATTERNS
[PATTERN_CATEGORY] { [pattern_name]: [description-and-requirements]; [implementation_note]: [specific-guidance] }

[Continue with additional pattern categories...]

## ANTI_PATTERNS
[ANTIPATTERN_CATEGORY] { [bad_pattern]: [description-of-what-not-to-do]; [alternative]: [what-to-do-instead] }

[Continue with additional anti-pattern categories...]

## TESTING_STATUS
[test_category]: [STATUS]; coverage: [percentage] ([details]); execution_time: [duration]; [additional_metrics]

## TEST_SUITE_BREAKDOWN
[test_suite_name] { TESTS: [count-and-status]; COVERAGE: [percentage]; SCOPE: [what-is-tested]; STATUS: [overall-health]; UPDATES: [recent-changes] }

[Continue with additional test suites...]

## TEST_COVERAGE_STRATEGY
[coverage_type] { APPROACH: [strategy]; SCOPE: [what-is-covered]; TARGET: [goal-percentage]; EXCLUSIONS: [what-is-excluded]; CONFIG: [configuration-files]; ACHIEVEMENT: [current-status] }

[Continue with additional coverage strategies...]

## CODE_QUALITY_STATUS
[quality_metric]: [status-and-date]; [foundation_assessment]: [rating]; [specific_area]: [assessment]; [compliance_metric]: [percentage]; [readiness_status]: [assessment-with-timeline]

## [DOMAIN_SPECIFIC_SECTIONS]
[Add sections specific to your project domain]
[Examples: API_ENDPOINTS, DATABASE_SCHEMA, DEPLOYMENT_STATUS, INTEGRATION_STATUS, etc.]

## CURRENT_STATUS [Updated: YYYY-MM-DDTHH:MM:SS UTC]

### [Current Focus Area] Status
- **Current**: [Current state description]
- **Previous Issue**: [Recently resolved problem]
- **Resolution**: [How it was fixed]

### [Quality/Progress Area]
- **[Metric 1]**: [Current status and trend]
- **[Metric 2]**: [Current status and numbers]
- **[Metric 3]**: [Implementation status]

### Recent Achievements [YYYY-MM-DDTHH:MM:SS UTC]
- **[Achievement 1]**: [Description and impact]
- **[Achievement 2]**: [Description and impact]
- **[Achievement 3]**: [Description and impact]

### [Performance/Infrastructure Area]
- **[Metric 1]**: [Current performance numbers]
- **[Metric 2]**: [Efficiency improvements]
- **[Metric 3]**: [Infrastructure status]

### Lessons Learned [YYYY-MM-DDTHH:MM:SS UTC]
- **[Lesson 1]**: [What was learned and why it matters]
- **[Lesson 2]**: [Pattern or anti-pattern discovered]
- **[Critical Learning]**: [Important insight for future development]

## NEXT_ACTION
**IMMEDIATE_PRIORITY**: [Most important current task]
**CURRENT_STATUS**: [Progress summary with metrics]
**CRITICAL_BLOCKER**: [Any blocking issues]
**NEXT_SESSION_PRIORITIES**: 
- [x] **COMPLETE**: [Completed task description]
- [x] **COMPLETE**: [Another completed task]
- [ ] **CRITICAL**: [Next critical task]
- [ ] **HIGH**: [Next high priority task]
- [ ] **MEDIUM**: [Medium priority task]
- [ ] **LOW**: [Low priority task]
**PLATFORM_STATUS**: [Overall system health summary]
**RAG_STATUS**: [Knowledge system status if applicable]

## PREVIOUS_NEXT_ACTION
[Archive of previous session priorities for historical context]

## SESSION_END_UPDATES [YYYY-MM-DDTHH:MM:SS UTC]
[Add session end updates here using the established format]
**COMPLETED_WORK**: [Summary of work completed in session]
**[DOMAIN]_ACHIEVEMENTS**: [Specific achievements in key areas]
**TECHNICAL_IMPLEMENTATION**: [Technical details of implementations]
**[STATUS]_STATUS**: [Current state of key systems]
**NEXT_SESSION_REQUIREMENTS**: [What needs to happen next]

[Continue session end updates with consistent format...]
