# [PROJECT NAME] PROJECT STATE DOCUMENT

# ⚠️ 🚨 CRITICAL UPDATE PROTOCOL - READ BEFORE ANY CHANGES 🚨 ⚠️

## ⛔ UPDATE_PROTOCOL ⛔
**🚨 ENFORCEMENT: MANDATORY - ZERO TOLERANCE FOR VIOLATIONS 🚨**
**⚠️ VIOLATION CONSEQUENCES: Protocol violations break historical continuity and project tracking ⚠️**
**📋 BEFORE ANY EDIT: Read this section completely. Follow format exactly. No exceptions.**

DATETIME_VERIFICATION: Use `ntpdate -q time.nist.gov` or `curl -s http://worldtimeapi.org/api/timezone/UTC` for verified UTC timestamps - NO HALLUCINATIONS ALLOWED
UPDATE_TYPES: STATUS_CHANGE|NEW_COMPONENT|ISSUE_RESOLUTION|ACHIEVEMENT|ARCHITECTURAL_DECISION|TECHNICAL_DEBT
APPEND_FORMAT: Add new entries to appropriate section using same compact syntax
STATUS_UPDATES: Modify existing STATUS field in place, append RESOLUTION or NOTES if needed
ACHIEVEMENT_FORMAT: achievement_YYYY_MM_DD_HH_MM_SS_description { verified_datetime: [system_clock_output]; scope: description; achievement: specific_outcome; impact: measurable_impact; files: [modified_files] }
ISSUE_FORMAT: issue_YYYY_MM_DD_HH_MM_SS_description { verified_datetime: [timestamp]; issue: specific_problem; impact: effect_on_system; status: current_state; location: [relevant_files]; priority: CRITICAL|HIGH|MEDIUM|LOW }
COMPONENT_UPDATE: Modify existing component entries in place, preserve all existing fields, add new fields with semicolon delimiter
ARCHITECTURAL_DECISION_UPDATE: Add new decision with rationale, implementation details, affected components
**🔒 NO_REMOVAL: NEVER remove historical data - only append or modify status 🔒**
**⏰ VERIFICATION_REQUIRED: Any datetime must be verified with actual system clock before entry ⚠️**

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
STATUS: COMPLETE|PARTIAL|BLOCKED|IN_PROGRESS|PLANNED|DEFERRED; PRIORITY: CRITICAL|HIGH|MEDIUM|LOW; CATEGORY: INFRA|CORE|TRANSPORT|TESTING|PACKAGING; REFS: [file/path] {config_key} <service_name>

## PROJECT_METADATA
PROJECT_ID: [project-name]; BUSINESS_MODEL: [business-model]; TIMELINE: [timeline]; TARGETS: [targets]; CURRENT_PHASE: [current-phase]; DEV_CADENCE: [dev-cadence]

## PHASE_STATUS
PHASE_1 { NAME: [Phase Name]; DURATION: [start-date] → [end-date]; STATUS: PLANNED; SYSTEM: [system-info]; DELIVERABLES: [deliverables]; DEPS: [dependencies] }

## COMPONENT_STATUS
INFRA_COMPONENTS { [component_name] { STATUS: PLANNED; PATTERN: [pattern]; FILES: [relevant_files]; COMMANDS: [commands] } }
CORE_COMPONENTS { [component_name] { STATUS: PLANNED; LOCATION: [file_path]; ENDPOINTS: [endpoints]; DEPS: [dependencies] } }
TRANSPORT_COMPONENTS { [component_name] { STATUS: PLANNED; LOCATION: [file_path]; ARCHITECTURE: [architecture]; FEATURES: [features] } }
TESTING_COMPONENTS { [component_name] { STATUS: PLANNED; SCOPE: [scope]; COVERAGE: [coverage]; PATTERNS: [patterns] } }

## ARCHITECTURAL_DECISIONS
[decision_name] { DECISION: [decision]; RATIONALE: [rationale]; IMPLEMENTATION: [implementation]; STATUS: PLANNED; FILES: [affected_files] }

## ACHIEVEMENTS
[achievement_YYYY_MM_DD_HH_MM_SS_description] { verified_datetime: [timestamp]; scope: [scope]; achievement: [achievement]; impact: [impact]; files: [files] }

## CURRENT_ISSUES
CRITICAL_ISSUES { }
HIGH_PRIORITY_ISSUES { }
MEDIUM_PRIORITY_ISSUES { }

## RESOLVED_ISSUES
[issue_YYYY_MM_DD_HH_MM_SS_description] { verified_datetime: [timestamp]; issue: [issue]; impact: [impact]; status: RESOLVED; location: [location]; resolution: [resolution]; priority: [priority] }

## TECHNICAL_DEBT
CRITICAL_DEBT { [debt_category] { ISSUE: [issue]; IMPACT: [impact]; SOLUTION: [solution]; LOCATIONS: [locations] } }
HIGH_PRIORITY_DEBT { [debt_category] { SCOPE: [scope]; REQUIREMENTS: [requirements] } }

## DEVELOPMENT_ENVIRONMENT
INFRASTRUCTURE_STATUS { [infrastructure_component]: [status]; [infrastructure_component]: [status] }
SERVICE_HEALTH { <service_name>: [status] (purpose); <service_name>: [status] (purpose) }
DEVELOPMENT_COMMANDS { [command_category]: [command] (description); [command_category]: [command] (description) }

## CRITICAL_PATTERNS
[PATTERN_CATEGORY] { [pattern_name]: [requirement]; [pattern_name]: [requirement] }

## ANTI_PATTERNS
CODE_ANTIPATTERNS { [antipattern]: [description]; [antipattern]: [description] }
ARCHITECTURE_ANTIPATTERNS { [antipattern]: [description]; [antipattern]: [description] }
TESTING_ANTIPATTERNS { [antipattern]: [description]; [antipattern]: [description] }

## TESTING_STATUS
unit_test_health: [status]; coverage: [coverage]; execution_time: [time]; integration_test_health: [status]; success_rate: [rate]; e2e_test_health: [status]; success_rate: [rate]

## TEST_SUITE_BREAKDOWN
[test_category] { TESTS: [test_count]; COVERAGE: [coverage]; SCOPE: [scope]; STATUS: [status] }

## TEST_COVERAGE_STRATEGY
unit_test_coverage { APPROACH: [approach]; SCOPE: [scope]; TARGET: [target]; EXCLUSIONS: [exclusions] }
integration_test_coverage { APPROACH: [approach]; SCOPE: [scope]; TARGET: [target]; EXCLUSIONS: [exclusions] }

## CODE_QUALITY_STATUS
style_analysis_completion: [date]; architectural_foundations: [status]; [category]: [status]; compliance_with_persona_standards: [percentage]; production_readiness: [status]; improvement_timeline: [timeline]

## CURRENT_STATUS [Updated: YYYY-MM-DDTHH:MM:SS UTC]

### [Primary Work Area] Status
- **Current**: [current_state]
- **Previous Issue**: [what_was_blocking_progress]
- **Resolution**: [how_it_was_resolved]

### [Quality/Progress Metrics]
- **[Metric 1]**: [status_with_numbers]
- **[Metric 2]**: [progress_made]

## NEXT_ACTION
**IMMEDIATE_PRIORITY**: [priority_description]
**CURRENT_STATUS**: [status_description]
**NEXT_SESSION_PRIORITIES**:
- [ ] **PRIORITY**: [task_description]
- [ ] **PRIORITY**: [task_description]

## PREVIOUS_NEXT_ACTION
**Priority 1**: [previous_priority_1]
**Priority 2**: [previous_priority_2]

## CURRENT_NEXT_ACTION
**Priority 1**: [current_priority_1]
**Priority 2**: [current_priority_2]

## SESSION_END_UPDATES [YYYY-MM-DDTHH:MM:SSZ]
**COMPLETED_WORK**: [summary_of_work_completed]
**ACHIEVEMENTS**: [key_achievements]
**TECHNICAL_IMPLEMENTATION**: [technical_details]
**NEXT_SESSION_REQUIREMENTS**: [what_needs_to_be_done_next]

---

**🔒 PROTOCOL COMPLIANCE REQUIRED: Follow ALL protocols exactly to maintain project continuity and cross-project intelligence.**
