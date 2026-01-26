// Admin view to inspect teachers and their courses, and create courses on their behalf.
import React, { useEffect, useMemo, useState } from 'react';
import api from '../services/api';

interface UserRow {
  id: number;
  username: string;
  email?: string;
  role?: string;
}

interface CourseRow {
  id: number;
  title: string;
  description?: string;
  created_at?: string;
  teacher?: number | UserRow;
}

const AdminCoursesOverview: React.FC = () => {
  const [teachers, setTeachers] = useState<UserRow[]>([]);
  const [courses, setCourses] = useState<CourseRow[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [expanded, setExpanded] = useState<Record<number, boolean>>({});
  const [creatingFor, setCreatingFor] = useState<number | null>(null);
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [creating, setCreating] = useState(false);

  const loadData = async () => {
    setLoading(true);
    setError(null);
    try {
      const [usersRes, coursesRes] = await Promise.all([
        api.get('accounts/users/?role=teacher'),
        api.get('courses/'),
      ]);
      const usersPayload = usersRes?.data;
      const usersList: UserRow[] = Array.isArray(usersPayload)
        ? usersPayload
        : Array.isArray(usersPayload?.results)
        ? usersPayload.results
        : [];
      const coursesPayload = coursesRes?.data;
      const coursesList: CourseRow[] = Array.isArray(coursesPayload)
        ? coursesPayload
        : Array.isArray(coursesPayload?.results)
        ? coursesPayload.results
        : [];
      setTeachers(usersList.filter((u) => (u as any).role === 'teacher'));
      setCourses(coursesList);
    } catch (e: any) {
      const msg = e?.response?.data?.detail || e?.message || 'Failed to load data';
      setError(typeof msg === 'string' ? msg : JSON.stringify(msg));
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const coursesByTeacher = useMemo(() => {
    const grouped: Record<number, CourseRow[]> = {};
    for (const c of courses) {
      const teacherId = typeof c.teacher === 'object' ? (c.teacher as UserRow)?.id : (c.teacher as number);
      if (!teacherId) continue;
      if (!grouped[teacherId]) grouped[teacherId] = [];
      grouped[teacherId].push(c);
    }
    return grouped;
  }, [courses]);

  const toggleExpanded = (teacherId: number) => {
    setExpanded((prev) => ({ ...prev, [teacherId]: !prev[teacherId] }));
  };

  const startCreateFor = (teacherId: number) => {
    setCreatingFor(teacherId);
    setTitle('');
    setDescription('');
  };

  const submitCreateFor = async () => {
    if (!creatingFor || !title.trim()) return;
    setCreating(true);
    setError(null);
    try {
      const payload: any = { title: title.trim(), description: description.trim() || undefined, teacher: creatingFor };
      await api.post('courses/', payload);
      setCreatingFor(null);
      setTitle('');
      setDescription('');
      await loadData();
    } catch (e: any) {
      const msg = e?.response?.data || e?.message || 'Failed to create course';
      setError(typeof msg === 'string' ? msg : JSON.stringify(msg));
    } finally {
      setCreating(false);
    }
  };

  return (
    <div className="dashboard-container">
      <h2 className="heading-xl">Admin: Teachers & Courses</h2>
      <p>Overview of teachers with their courses. Create courses for teachers as needed.</p>

      {error && <div className="auth-error">{error}</div>}
      {loading ? (
        <p>Loading data…</p>
      ) : (
        <table className="table">
          <thead>
            <tr>
              <th>Teacher</th>
              <th>Email</th>
              <th>Course Count</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {teachers.map((t) => {
              const list = coursesByTeacher[t.id] || [];
              const isOpen = !!expanded[t.id];
              return (
                <React.Fragment key={t.id}>
                  <tr>
                    <td>{t.username}</td>
                    <td>{t.email || ''}</td>
                    <td>{list.length}</td>
                    <td>
                      <button className="button" onClick={() => toggleExpanded(t.id)} aria-label="Toggle courses" title="Toggle courses">
                        {isOpen ? 'Hide Courses' : 'Show Courses'}
                      </button>
                      <button className="button" onClick={() => startCreateFor(t.id)} aria-label="Create for teacher" title="Create for teacher" style={{ marginLeft: 8 }}>
                        Create Course
                      </button>
                    </td>
                  </tr>
                  {isOpen && (
                    <tr>
                      <td colSpan={4}>
                        {list.length === 0 ? (
                          <p>No courses for this teacher yet.</p>
                        ) : (
                          <table className="table" style={{ marginTop: 8 }}>
                            <thead>
                              <tr>
                                <th>ID</th>
                                <th>Title</th>
                                <th>Description</th>
                                <th>Created</th>
                              </tr>
                            </thead>
                            <tbody>
                              {list.map((c) => (
                                <tr key={c.id}>
                                  <td>{c.id}</td>
                                  <td>{c.title}</td>
                                  <td>{c.description || ''}</td>
                                  <td>{c.created_at || ''}</td>
                                </tr>
                              ))}
                            </tbody>
                          </table>
                        )}
                      </td>
                    </tr>
                  )}
                  {creatingFor === t.id && (
                    <tr>
                      <td colSpan={4}>
                        <div className="card" style={{ display: 'flex', gap: 8, alignItems: 'center', flexWrap: 'wrap' }}>
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
                          <button className="button" disabled={creating || !title.trim()} onClick={submitCreateFor} aria-label="Create course for teacher" title="Create course for teacher">
                            {creating ? 'Creating…' : 'Create'}
                          </button>
                          <button className="button" onClick={() => setCreatingFor(null)} aria-label="Cancel" title="Cancel">
                            Cancel
                          </button>
                        </div>
                      </td>
                    </tr>
                  )}
                </React.Fragment>
              );
            })}
          </tbody>
        </table>
      )}
    </div>
  );
};

export default AdminCoursesOverview;
