import React, { useEffect, useState } from 'react';
import './TeacherDashboard.css';
import api from '../services/api';
import { useAuth } from '../auth/AuthContext';
import { useNavigate } from 'react-router-dom';

interface CourseRow {
  id: number;
  title: string;
  description?: string;
  created_at?: string;
}

interface LessonRow {
  id: number;
  title: string;
  content: string;
  order: number;
  // course comes from the API as a nested object; we only care about its id here
  course?: {
    id: number;
  };
}

const TeacherDashboard: React.FC = () => {
  const { logout } = useAuth();
  const navigate = useNavigate();

  const [courses, setCourses] = useState<CourseRow[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [creating, setCreating] = useState(false);
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [editingId, setEditingId] = useState<number | null>(null);
  const [editTitle, setEditTitle] = useState('');
  const [editDescription, setEditDescription] = useState('');
  const [savingEdit, setSavingEdit] = useState(false);
  const [deletingId, setDeletingId] = useState<number | null>(null);

  // Lessons grouped by course id for quick lookup when managing lessons per course.
  const [lessonsByCourse, setLessonsByCourse] = useState<Record<number, LessonRow[]>>({});
  const [openCourseId, setOpenCourseId] = useState<number | null>(null);
  const [newLessonTitle, setNewLessonTitle] = useState('');
  const [newLessonContent, setNewLessonContent] = useState('');
  const [creatingLessonFor, setCreatingLessonFor] = useState<number | null>(null);
  const [deletingLessonId, setDeletingLessonId] = useState<number | null>(null);

  // Load only the courses owned by the logged-in teacher; handles paginated or plain arrays.
  const fetchMyCourses = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await api.get('courses/my/');
      const payload = res?.data;
      const list: CourseRow[] = Array.isArray(payload)
        ? payload
        : Array.isArray(payload?.results)
        ? (payload.results as CourseRow[])
        : [];
      setCourses(list);
    } catch (e: any) {
      setError(e?.message || 'Failed to load courses');
    } finally {
      setLoading(false);
    }
  };

  // Load all lessons for this teacher so we can filter them per course in the UI.
  const fetchMyLessons = async () => {
    try {
      const res = await api.get('lessons/');
      const payload = res?.data;
      const list: LessonRow[] = Array.isArray(payload)
        ? payload
        : Array.isArray(payload?.results)
        ? (payload.results as LessonRow[])
        : [];
      const grouped: Record<number, LessonRow[]> = {};
      list.forEach((lesson) => {
        const courseId = lesson.course?.id;
        if (!courseId) return;
        if (!grouped[courseId]) grouped[courseId] = [];
        grouped[courseId].push(lesson);
      });
      // Ensure lessons are ordered within each course
      Object.keys(grouped).forEach((key) => {
        const cid = Number(key);
        grouped[cid] = grouped[cid].slice().sort((a, b) => a.order - b.order);
      });
      setLessonsByCourse(grouped);
    } catch (e: any) {
      // If lessons fail to load, we still allow course management; just show no lessons.
      console.error('Failed to load lessons for teacher dashboard:', e);
    }
  };

  useEffect(() => {
    // Initial page load: populate data so you immediately see what you own.
    fetchMyCourses();
    fetchMyLessons();
  }, []);

  const beginEdit = (course: CourseRow) => {
    setError(null);
    setEditingId(course.id);
    setEditTitle(course.title);
    setEditDescription(course.description || '');
  };

  const cancelEdit = () => {
    setEditingId(null);
    setEditTitle('');
    setEditDescription('');
  };

  const saveEdit = async () => {
    if (!editingId || !editTitle.trim()) return;
    setSavingEdit(true);
    setError(null);
    try {
      const payload = {
        title: editTitle.trim(),
        description: editDescription.trim() || undefined,
      };
      const res = await api.patch(`courses/${editingId}/`, payload);
      setCourses((prev) =>
        prev.map((c) => (c.id === editingId ? { ...c, ...res.data } : c))
      );
      cancelEdit();
    } catch (e: any) {
      const msg = e?.response?.data?.detail || e?.message || 'Failed to update course';
      setError(typeof msg === 'string' ? msg : JSON.stringify(msg));
    } finally {
      setSavingEdit(false);
    }
  };

  const deleteCourse = async (id: number) => {
    if (!window.confirm('Are you sure you want to delete this course?')) return;
    setDeletingId(id);
    setError(null);
    try {
      await api.delete(`courses/${id}/`);
      setCourses((prev) => prev.filter((c) => c.id !== id));
    } catch (e: any) {
      const msg = e?.response?.data?.detail || e?.message || 'Failed to delete course';
      setError(typeof msg === 'string' ? msg : JSON.stringify(msg));
    } finally {
      setDeletingId(null);
    }
  };

  return (
    <div className="dashboard-container">
      <div className="dashboard-header">
        <h2 className="heading-xl">Teacher Dashboard</h2>
        <button className="button" onClick={() => { logout(); navigate('/'); }}>
          Logout
        </button>
      </div>
      <p>Welcome, teacher! Here you can manage your courses and lessons.</p>

      <div className="card card--spaced">
        <h3>Create Course</h3>
        <div className="create-controls">
          <input
            aria-label="Course title"
            type="text"
            placeholder="Title"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
          />
          <input
            aria-label="Course description"
            type="text"
            placeholder="Description (optional)"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
          />
          <button
            className="button"
            disabled={creating || !title.trim()}
            onClick={async () => {
              setError(null);
              setCreating(true);
              try {
                const payload = {
                  title: title.trim(),
                  description: description.trim() || undefined,
                };
                await api.post('courses/', payload);
                setTitle('');
                setDescription('');
                await fetchMyCourses();
              } catch (e: any) {
                const data = e?.response?.data;
                if (data) {
                  setError(typeof data === 'string' ? data : JSON.stringify(data));
                } else {
                  const msg = e?.message || 'Failed to create course';
                  setError(typeof msg === 'string' ? msg : JSON.stringify(msg));
                }
              } finally {
                setCreating(false);
              }
            }}
            aria-label="Create course"
            title="Create course"
          >
            {creating ? 'Creating…' : 'Create'}
          </button>
        </div>
      </div>

      {error && <div className="auth-error">{error}</div>}
      {loading ? (
        <p>Loading your courses...</p>
      ) : courses.length === 0 ? (
        <p>You have no courses yet. Create one to get started.</p>
      ) : (
        <table className="table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Title</th>
              <th>Description</th>
              <th>Created</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {courses.map((c) => (
              <React.Fragment key={c.id}>
                <tr>
                  <td>{c.id}</td>
                  <td>
                    {editingId === c.id ? (
                      <input
                        type="text"
                        aria-label="Edit course title"
                        value={editTitle}
                        onChange={(e) => setEditTitle(e.target.value)}
                      />
                    ) : (
                      c.title
                    )}
                  </td>
                  <td>
                    {editingId === c.id ? (
                      <input
                        type="text"
                        aria-label="Edit course description"
                        value={editDescription}
                        onChange={(e) => setEditDescription(e.target.value)}
                      />
                    ) : (
                      c.description || ''
                    )}
                  </td>
                  <td>{c.created_at || ''}</td>
                  <td>
                    {editingId === c.id ? (
                      <>
                        <button
                          className="button"
                          disabled={savingEdit || !editTitle.trim()}
                          onClick={saveEdit}
                        >
                          {savingEdit ? 'Saving…' : 'Save'}
                        </button>
                        <button className="button ml-2" onClick={cancelEdit}>
                          Cancel
                        </button>
                      </>
                    ) : (
                      <>
                        <button
                          className="button"
                          onClick={() => beginEdit(c)}
                          aria-label="Edit course"
                          title="Edit course"
                        >
                          Edit
                        </button>
                        <button
                          className="button ml-2"
                          onClick={() => deleteCourse(c.id)}
                          disabled={deletingId === c.id}
                          aria-label="Delete course"
                          title="Delete course"
                        >
                          {deletingId === c.id ? 'Deleting…' : 'Delete'}
                        </button>
                        <button
                          className="button ml-2"
                          onClick={async () => {
                            setError(null);
                            // If we haven't loaded lessons yet (e.g. first visit), fetch them.
                            if (!lessonsByCourse[c.id]) {
                              await fetchMyLessons();
                            }
                            setOpenCourseId(openCourseId === c.id ? null : c.id);
                            setNewLessonTitle('');
                            setNewLessonContent('');
                          }}
                          aria-label="Manage lessons for this course"
                          title="Manage lessons for this course"
                        >
                          {openCourseId === c.id ? 'Hide Lessons' : 'Manage Lessons'}
                        </button>
                      </>
                    )}
                  </td>
                </tr>
                {openCourseId === c.id && (
                  <tr>
                    <td colSpan={5}>
                      <div className="lessons-panel">
                        <h4>Lessons for this course</h4>
                        <ul className="lessons-list">
                          {(lessonsByCourse[c.id] || []).length === 0 ? (
                            <li className="lessons-list-item">No lessons yet for this course.</li>
                          ) : (
                            (lessonsByCourse[c.id] || []).map((lesson) => (
                              <li key={lesson.id} className="lessons-list-item-spaced">
                                <span className="lesson-title-text">
                                  {lesson.order}. {lesson.title}
                                </span>
                                <button
                                  className="button ml-2"
                                  onClick={async () => {
                                    if (!window.confirm('Delete this lesson? This cannot be undone.')) return;
                                    setDeletingLessonId(lesson.id);
                                    try {
                                      await api.delete(`lessons/${lesson.id}/`);
                                      setLessonsByCourse((prev) => {
                                        const copy = { ...prev };
                                        copy[c.id] = (copy[c.id] || []).filter((l) => l.id !== lesson.id);
                                        return copy;
                                      });
                                    } catch (e: any) {
                                      const msg =
                                        e?.response?.data?.detail || e?.message || 'Failed to delete lesson';
                                      setError(typeof msg === 'string' ? msg : JSON.stringify(msg));
                                    } finally {
                                      setDeletingLessonId(null);
                                    }
                                  }}
                                  disabled={deletingLessonId === lesson.id}
                                >
                                  {deletingLessonId === lesson.id ? 'Deleting…' : 'Delete Lesson'}
                                </button>
                              </li>
                            ))
                          )}
                        </ul>
                        <div className="lesson-create-form">
                          <h5>Add a new lesson</h5>
                          <input
                            type="text"
                            aria-label="Lesson title"
                            placeholder="Lesson title"
                            value={newLessonTitle}
                            onChange={(e) => setNewLessonTitle(e.target.value)}
                          />
                          <textarea
                            aria-label="Lesson content"
                            placeholder="Lesson content (HTML or plain text)"
                            value={newLessonContent}
                            onChange={(e) => setNewLessonContent(e.target.value)}
                            rows={4}
                          />
                          <button
                            className="button mt-2"
                            disabled={
                              !newLessonTitle.trim() ||
                              !newLessonContent.trim() ||
                              creatingLessonFor === c.id
                            }
                            onClick={async () => {
                              if (!newLessonTitle.trim() || !newLessonContent.trim()) return;
                              setError(null);
                              setCreatingLessonFor(c.id);
                              try {
                                const currentLessons = lessonsByCourse[c.id] || [];
                                const nextOrder =
                                  currentLessons.length > 0
                                    ? Math.max(...currentLessons.map((l) => l.order)) + 1
                                    : 1;
                                const payload = {
                                  course_id: c.id,
                                  title: newLessonTitle.trim(),
                                  content: newLessonContent.trim(),
                                  order: nextOrder,
                                };
                                const res = await api.post('lessons/', payload);
                                const created: LessonRow = res.data;
                                setLessonsByCourse((prev) => {
                                  const copy = { ...prev };
                                  const existing = copy[c.id] || [];
                                  copy[c.id] = [...existing, created].sort((a, b) => a.order - b.order);
                                  return copy;
                                });
                                setNewLessonTitle('');
                                setNewLessonContent('');
                              } catch (e: any) {
                                const data = e?.response?.data;
                                if (data) {
                                  setError(typeof data === 'string' ? data : JSON.stringify(data));
                                } else {
                                  const msg = e?.message || 'Failed to create lesson';
                                  setError(typeof msg === 'string' ? msg : JSON.stringify(msg));
                                }
                              } finally {
                                setCreatingLessonFor(null);
                              }
                            }}
                          >
                            {creatingLessonFor === c.id ? 'Creating Lesson…' : 'Create Lesson'}
                          </button>
                        </div>
                      </div>
                    </td>
                  </tr>
                )}
              </React.Fragment>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
};

export default TeacherDashboard;
