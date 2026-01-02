# Courses Page Enhancement Plan

Purpose: keep the Courses page and add value beyond the homepage by revealing richer course context inline (accordion or modal) without navigating away. This document captures the implementation plan, data needs, UI structure, styling approach, and code sketches so it can be built quickly later.

## Goals
- Make each course tile expandable (accordion) or open a modal with more detail.
- Show concise syllabus/learning outcomes, lesson count and completion summary, quiz availability, and coding focus/stack.
- Keep existing navigation intact; reduce context switches by avoiding page redirects.
- Preserve current styling language (cool blues/greys, shared `.button`, cards, responsive grids).

## Data requirements (no new backend endpoints)
- Courses list: `GET /api/courses/` (already used).
- Course detail: `GET /api/courses/{id}/` (for description/teacher if needed).
- Lessons for grouping: `GET /api/lessons/` (already used) — filter client-side by course.
- Optional: quiz presence per lesson via `quiz_id` on lesson payload (already present in serializer).

## UI behaviors
- Default view: same grid of course cards.
- Interaction: clicking a card (or a “More details” button) expands inline (accordion) or opens a modal.
- Content inside detail view:
  - Short blurb: “What you’ll build/learn”.
  - Lesson summary: total lessons, completed count (if enrolled), list with status chips.
  - Quiz note: show if any lesson has a `quiz_id`.
  - CTA: “View Lessons” (if enrolled) and “Enroll” (if not enrolled).
- Accessibility: focus trap in modal; ESC to close; arrow/tab navigation preserved. For accordion, ensure buttons are `<button>` and aria-expanded/aria-controls are set.

## State and data flow (frontend)
- Keep existing state in `Profile.tsx`: `courses`, `enrolledCourseIds`, `courseLessons`, `openDropdown`.
- Add `expandedCourseId` (for accordion) or `modalCourseId` (for modal).
- Reuse `courseLessons[courseId]` for lesson listings; compute completion counts from `is_completed` flags.
- If detailed course description is needed, fetch on-demand (`/api/courses/{id}/`) when expanding, cache in a `courseDetails` map.

## Component sketch (accordion approach)
```tsx
// Inside course card
<button
  className="button"
  onClick={() => setExpandedCourseId(expandedCourseId === course.id ? null : course.id)}
>
  {expandedCourseId === course.id ? 'Hide details' : 'More details'}
</button>
{expandedCourseId === course.id && (
  <div className="course-detail-panel">
    <p className="course-blurb">What you’ll build: {courseDetails[course.id]?.blurb || 'TBD'}</p>
    <p className="course-meta">Lessons: {lessons.length} • Completed: {lessons.filter(l => l.is_completed).length}</p>
    {lessons.length > 0 && (
      <ul className="lesson-list">
        {lessons.map(lesson => (
          <li key={lesson.id} className="lesson-chip">
            {lesson.title}
            {lesson.is_completed && <span className="pill pill--success">Done</span>}
            {lesson.quiz_id && <span className="pill pill--info">Quiz</span>}
          </li>
        ))}
      </ul>
    )}
    <div className="detail-actions">
      <button className="button" disabled={!isEnrolled} onClick={() => setOpenDropdown(openDropdown === course.id ? null : course.id)}>
        View Lessons
      </button>
      {!isEnrolled && (
        <button className="button button--primary" onClick={() => handleEnroll(course.id)} disabled={enrolling === course.id}>
          {enrolling === course.id ? 'Enrolling...' : 'Enroll'}
        </button>
      )}
    </div>
  </div>
)}
```

## Component sketch (modal approach)
```tsx
// Trigger
<button className="button" onClick={() => setModalCourseId(course.id)}>
  More details
</button>

// Modal shell
{modalCourseId && (
  <div className="modal-backdrop" onClick={() => setModalCourseId(null)}>
    <div className="modal" role="dialog" aria-modal="true" onClick={e => e.stopPropagation()}>
      <button className="modal-close" onClick={() => setModalCourseId(null)}>×</button>
      <h3>{course.title}</h3>
      <p className="course-blurb">{courseDetails[course.id]?.blurb || course.description}</p>
      <p className="course-meta">Lessons: {lessons.length} • Completed: {completed}/{lessons.length}</p>
      <div className="lesson-list modal-list">
        {lessons.map(lesson => (
          <div key={lesson.id} className="lesson-chip">
            {lesson.title}
            {lesson.is_completed && <span className="pill pill--success">Done</span>}
            {lesson.quiz_id && <span className="pill pill--info">Quiz</span>}
          </div>
        ))}
      </div>
      <div className="detail-actions">
        <button className="button" disabled={!isEnrolled} onClick={() => { setOpenDropdown(course.id); setModalCourseId(null); }}>
          View Lessons
        </button>
        {!isEnrolled && (
          <button className="button button--primary" onClick={() => handleEnroll(course.id)} disabled={enrolling === course.id}>
            {enrolling === course.id ? 'Enrolling...' : 'Enroll'}
          </button>
        )}
      </div>
    </div>
  </div>
)}
```

## Styling notes (fit current system)
- Use existing palette: text `#334e68`, accents `#486581`, primary `#2563eb`, success `#4fbb6b`, error `#e11d48`.
- Reuse `.button`; add modifiers:
```css
.button--primary { background: #2563eb; color: #fff; }
.pill { display: inline-block; padding: 0.1rem 0.4rem; border-radius: 999px; font-size: 0.75rem; }
.pill--success { background: #e3f9e5; color: #157f3d; }
.pill--info { background: #e0f2fe; color: #075985; }
.course-detail-panel { margin-top: 0.75rem; padding: 1rem; background: #f7f9fb; border-radius: 8px; box-shadow: 0 2px 8px rgba(51,78,104,0.08); }
.lesson-list { list-style: none; padding: 0; margin: 0.5rem 0 0; display: grid; gap: 0.35rem; }
.lesson-chip { background: #fff; border: 1px solid #d9e2ec; border-radius: 6px; padding: 0.5rem 0.75rem; display: flex; gap: 0.5rem; align-items: center; }
.modal-backdrop { position: fixed; inset: 0; background: rgba(0,0,0,0.4); display: grid; place-items: center; z-index: 1000; }
.modal { background: #fff; padding: 1.25rem; border-radius: 10px; width: min(720px, 90vw); max-height: 90vh; overflow: auto; box-shadow: 0 10px 40px rgba(0,0,0,0.12); }
.modal-close { background: transparent; border: none; font-size: 1.25rem; position: absolute; top: 0.75rem; right: 0.75rem; cursor: pointer; }
.detail-actions { display: flex; gap: 0.75rem; flex-wrap: wrap; margin-top: 1rem; }
```

## Small backend consideration
- None required if using existing endpoints. If lesson payloads ever omit `quiz_id`, ensure the serializer keeps it exposed (`LessonSerializer` already emits `quiz_id`).

## Rollout steps (when ready to build)
1. Add state (`expandedCourseId` or `modalCourseId`) and detail cache in `Profile.tsx`.
2. Add UI block to course cards for detail trigger and panel/modal.
3. Add styling snippets to `src/index.css` (or a scoped CSS module) using the above tokens.
4. Optional: add `courseBlurb` content in seed data or hardcode a short map per course id.
5. Test flows: enrolled student, non-enrolled student, teacher/admin (should still see detail, but enroll CTA can hide for staff if desired).
6. Accessibility pass: focus trap in modal, aria attributes on accordion buttons, ESC to close modal.

## Why document vs build now
- Captures clear scope and approach without adding late-cycle risk.
- Can be implemented quickly later with minimal backend changes.
- Shows planning and UX improvement intent beyond the current homepage overlap.
