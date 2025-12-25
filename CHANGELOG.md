# CHANGELOG

<!-- version list -->

## v1.0.0 (2025-12-25)

### Features - 1.0 Stable Release 🎉

**Complete AI Tools Coverage**
- **feat(github)**: Add AI tools for GitHub connector ([#66](https://github.com/jbcom/vendor-connectors/pull/66))
  - Repository operations, teams, org members, file operations
  - LangChain, CrewAI, Strands support
- **feat(google)**: Add AI-callable tools for Google connector ([#65](https://github.com/jbcom/vendor-connectors/pull/65))
  - List projects, services, billing accounts, Workspace users/groups
  - Framework adapters for all AI platforms
- **feat(slack)**: Add AI framework tools for Slack operations ([#64](https://github.com/jbcom/vendor-connectors/pull/64))
  - Send messages, list channels/users, get history
  - Complete bot integration support
- **feat(vault)**: Add AI tools for Vault connector ([#63](https://github.com/jbcom/vendor-connectors/pull/63))
  - Read/list secrets, generate AWS credentials
  - Secure credential management
- **feat(zoom)**: Add AI tools for Zoom connector ([#62](https://github.com/jbcom/vendor-connectors/pull/62))
  - List/get users, list/get meetings
  - Complete meeting management

**Dependencies & Stability**
- **fix**: Update directed-inputs-class dependency to use semver constraints ([#39](https://github.com/jbcom/vendor-connectors/issues/39))
  - Changed from date-based versioning to `>=1.0.0`
  - Ensures ecosystem compatibility

**What 1.0 Means**
- ✅ Stable API with semantic versioning commitment
- ✅ All connectors have AI tools (AWS, Google, GitHub, Slack, Vault, Zoom, Meshy, Anthropic, Cursor)
- ✅ Comprehensive test coverage (>62%)
- ✅ Production-ready with battle-tested patterns
- ✅ Full documentation and examples

### Breaking Changes
None - this is a stabilization release that commits to API stability going forward.

### Testing
- 20+ tests per connector for AI tools
- All tests use proper mocking (no live API calls)
- CI passing on all branches

## v0.2.0 (2025-12-07)

### Features

- **connectors**: Add Cursor and Anthropic connectors
  ([#16](https://github.com/jbcom/vendor-connectors/pull/16),
  [`2edc23f`](https://github.com/jbcom/vendor-connectors/commit/2edc23f3e706919dff4196c489773442cdf8cb31))


## v0.1.1 (2025-12-07)

### Bug Fixes

- Restore working Dockerfile with Go 1.25.3 and correct process-compose install
  ([`aa10854`](https://github.com/jbcom/vendor-connectors/commit/aa10854a11ed0e87e1450743f7925acf8b5bcf4c))


## v0.1.0 (2025-12-06)

- Initial Release
