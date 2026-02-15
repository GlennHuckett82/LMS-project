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

// Simple teacher control panel: lists your courses and lets you create new ones.
// Kept intentionally direct so a beginner can trace data loading and creation in one file.
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

  useEffect(() => {
    // Initial page load: populate the table so you immediately see what you own.
    fetchMyCourses();
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
        <button className="button" onClick={() => { logout(); navigate('/'); }}>Logout</button>
      </div>
      <p>Welcome, teacher! Here you can manage your courses.</p>

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
                const payload = { title: title.trim(), description: description.trim() || undefined };
                await api.post('courses/', payload);
                setTitle('');
                setDescription('');
                await fetchMyCourses();
              } catch (e: any) {
                const msg = e?.response?.data?.detail || e?.message || 'Failed to create course';
                setError(typeof msg === 'string' ? msg : JSON.stringify(msg));
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
              <tr key={c.id}>
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
                    </>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
};

export default TeacherDashboard;
