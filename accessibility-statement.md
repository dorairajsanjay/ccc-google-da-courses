# Accessibility Compliance Statement
## CCC Google Data Analytics Certificate Courses

---

## Commitment to Accessibility

The CCC Google Data Analytics Certificate courses are designed to be accessible
to all students, including those with disabilities. We follow the Web Content
Accessibility Guidelines (WCAG) 2.0 Level AA as our standard.

---

## Accessibility Responsibilities

Accessibility in these courses is a shared responsibility across three platforms:

### 1. Canvas LMS (Learning Management System)

**Handled by Canvas/Instructure:**
- Screen reader compatibility (Canvas is VPAT-certified)
- Keyboard navigation throughout the LMS interface
- High contrast mode support
- Alternative text for Canvas-generated UI elements
- Mobile responsive design
- Closed captioning support for Canvas media

**Canvas accessibility resources:**
- [Canvas Accessibility Standards](https://www.instructure.com/canvas/accessibility)
- [Canvas VPAT (Voluntary Product Accessibility Template)](https://www.instructure.com/canvas/vpat)

### 2. Coursera Platform

**Handled by Coursera:**
- Video captions and transcripts for all Google course videos
- Screen reader compatibility for Coursera interface
- Keyboard navigation on Coursera platform
- Mobile app accessibility features

**Coursera accessibility resources:**
- [Coursera Accessibility Statement](https://www.coursera.org/about/accessibility)

**Note:** If a student encounters accessibility barriers on Coursera, they should
contact Coursera support and inform their instructor. Alternative arrangements
may be needed.

### 3. Course Content (Our Responsibility)

**What we have done:**
- All HTML content uses semantic headings (h2, h3, h4) in proper hierarchy
- All data tables include header cells (`<th>` elements)
- Link text is descriptive (no "click here" links)
- Content is structured with lists and headings for screen reader navigation
- No content relies solely on color to convey meaning
- All quiz question text is in accessible HTML format
- Page content is compatible with browser zoom up to 200%

**Automated checks:**
The course build system includes an automated accessibility audit that checks for:
- Images without alt text
- Non-descriptive link text
- Heading hierarchy violations
- Tables without header cells

**Known limitations:**
- Placeholder URLs (e.g., `[NOTEBOOKLM_PODCAST_URL]`) need to be replaced with
  accessible resources before use
- Instructor-added content (announcements, uploaded files) is the instructor's
  responsibility to make accessible
- External resources linked from course pages may have varying accessibility levels

---

## Student Accommodations

Students who need accommodations should:

1. Contact their institution's Disability Resource Center (DRC) as early as possible
2. Provide accommodation letters to their instructor
3. Discuss specific needs with their instructor during office hours
4. Report any accessibility barriers they encounter in the course content

**Common accommodations for online courses:**
- Extended time on quizzes and exams
- Alternative format for assignments (audio, video instead of written)
- Screen reader-compatible versions of uploaded documents
- Captioned or transcribed media content
- Flexible deadlines

---

## Reporting Accessibility Issues

If you encounter an accessibility barrier in the course content (not Canvas or Coursera):

1. Note the specific page, assignment, or resource with the issue
2. Describe the barrier and the assistive technology you are using
3. Contact your instructor or the course development team
4. We will work to resolve the issue or provide an alternative

---

## WCAG 2.0 Conformance Details

| Guideline | Status | Notes |
|-----------|--------|-------|
| 1.1 Text Alternatives | Conformant | Alt text on images, descriptive links |
| 1.2 Time-based Media | Partial | Coursera handles video captions; NotebookLM resources TBD |
| 1.3 Adaptable | Conformant | Semantic HTML, proper heading hierarchy |
| 1.4 Distinguishable | Conformant | No color-only information, resizable text |
| 2.1 Keyboard Accessible | Conformant | Canvas and HTML content keyboard navigable |
| 2.2 Enough Time | Conformant | Unlimited quiz attempts by default |
| 2.3 Seizures | Conformant | No flashing content |
| 2.4 Navigable | Conformant | Descriptive headings and link text |
| 3.1 Readable | Conformant | Clear language, defined terms |
| 3.2 Predictable | Conformant | Consistent navigation through modules |
| 3.3 Input Assistance | Conformant | Clear instructions on assignments |
| 4.1 Compatible | Conformant | Valid HTML, ARIA-compatible |
