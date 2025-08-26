# Awesome Design Assets for Developers - Repository Instructions

**Always reference these instructions first and fallback to search or bash commands only when you encounter unexpected information that does not match the info here.**

This is a documentation-only "Awesome List" repository containing a curated collection of design resources for developers. The repository follows the standard awesome list format with markdown files and no executable code.

## Repository Structure

**Working files:**
- `README.md` - English version of the curated list (120 lines)
- `README.zh.md` - Chinese version of the curated list (120 lines)  
- `banner.svg` - Visual banner for the repository (232KB SVG file)
- `.gitignore` - Git ignore file

**Categories in the list:**
- UI Libraries (12 resources)
- Icons (11 resources)  
- Illustrations (8 resources)
- Templates (4 resources)
- Photography (8 resources)
- Fonts (6 resources)
- Colors (6 resources)
- Tools (12 resources)
- Books (2 resources)
- Communities (4 resources)

## Setup and Installation

Install required tools for validation:
- `npm install markdown-link-check` - For link validation (takes 5-10 seconds)

## Validation Commands

**CRITICAL - Link Validation:**
- Run `npx markdown-link-check README.md` - Validates all links in English README. Takes 1-2 minutes. NEVER CANCEL.
- Run `npx markdown-link-check README.zh.md` - Validates all links in Chinese README. Takes 1-2 minutes. NEVER CANCEL.
- **Expected:** Link checking may fail due to network restrictions or temporary outages. This is normal - document any consistently failing links.

**Format Validation:**
- Each resource follows format: `- [Name](URL) - Description`
- Paid resources are marked with 💵 emoji
- Internal links use `#anchor-format`
- Descriptions should be concise but informative

## Common Tasks

**Adding new resources:**
1. Add to appropriate category in both `README.md` and `README.zh.md`
2. Follow the exact format: `- [Resource Name](https://url.com) - Brief description.`
3. Maintain alphabetical order within categories when possible
4. Add 💵 emoji for paid resources
5. Always validate links before adding: `curl -I https://url.com`

**Updating existing resources:**
1. Edit both English and Chinese versions
2. Preserve the link format and description style
3. Validate the updated link works

**Link maintenance:**
1. Run link validation regularly
2. Update or remove broken links
3. Document persistent issues in PR descriptions

## Validation Workflow

**Before making changes:**
1. `npm install markdown-link-check` (if not already installed)
2. Check current link status: `npx markdown-link-check README.md --quiet`
3. Note any existing broken links (not your responsibility to fix unless related to your changes)

**After making changes:**
1. Validate markdown format visually
2. Check new/modified links: `curl -I https://newurl.com` 
3. Run full link validation: `npx markdown-link-check README.md` - NEVER CANCEL, takes 1-2 minutes
4. Run Chinese version validation: `npx markdown-link-check README.zh.md` - NEVER CANCEL, takes 1-2 minutes
5. Document any validation failures in your PR

## Network Limitations

**Important:** The sandbox environment has limited internet access. Link validation may fail due to:
- Blocked domains
- Network timeouts
- Temporary service outages

This is expected - document validation attempts and results rather than trying to fix network issues.

## File Management

**What NOT to commit:**
- `node_modules/` - Automatically excluded by .gitignore
- `package-lock.json` - Build artifact, excluded by .gitignore
- Temporary files (*.tmp, *.temp)

**What TO commit:**
- Changes to `README.md` and `README.zh.md`
- Updates to `.gitignore` if needed
- New `banner.svg` if updated

## Quality Guidelines

**Content standards:**
- Maintain high-quality, relevant resources only
- Ensure descriptions are accurate and helpful
- Remove outdated or dead resources
- Keep both language versions synchronized

**Formatting standards:**
- Consistent bullet point format with `- `
- Proper markdown link syntax `[text](url)`
- Consistent spacing and line breaks
- Categories should have clear headers

## Common File Locations Reference

```
Repository Root: /home/runner/work/awesome-design-dev/awesome-design-dev/
├── README.md (main English list)
├── README.zh.md (Chinese translation)
├── banner.svg (header image)
├── .gitignore (git exclusions)
├── .github/copilot-instructions.md (this file)
├── package.json (npm dependencies)
└── node_modules/ (excluded from git)
```

## Sample Commands for Reference

**File operations:**
- `cat README.md | head -20` - View first 20 lines
- `grep -c "http" README.md` - Count links (should be ~73)
- `wc -l README.md` - Count lines (should be ~120)

**Link validation:**
- `npx markdown-link-check README.md --quiet` - Quick validation summary
- `curl -I https://example.com` - Test single link manually

**Git operations:**
- `git status` - Check repository state  
- `git diff README.md` - View changes to main file
- Always use the report_progress tool for commits, not direct git commands

## Troubleshooting

**If link validation fails:**
1. Note the specific failing URLs
2. Test manually with `curl -I <URL>`
3. Check if it's a network issue or actual broken link
4. Document findings in PR description
5. Do NOT spend time trying to fix external network issues

**If files seem corrupted:**
1. Check file sizes: `ls -la`
2. Verify content: `head README.md`
3. Compare with git: `git diff`
4. Revert if necessary: `git checkout README.md`

## Validation Timing Expectations

- `npm install markdown-link-check`: 5-10 seconds
- `npx markdown-link-check README.md`: 1-2 minutes - NEVER CANCEL
- `npx markdown-link-check README.zh.md`: 1-2 minutes - NEVER CANCEL
- Manual link testing with curl: 2-5 seconds per URL

**Remember: This is a documentation repository with no build process, tests, or executable code. Focus on content quality and link maintenance rather than traditional software development workflows.**