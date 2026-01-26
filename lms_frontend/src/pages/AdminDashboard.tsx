import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../services/api';
import { useAuth } from '../auth/AuthContext';

interface UserRow {
  id: number;
  username: string;
  email?: string;
  role?: string;
  is_staff?: boolean;
  is_superuser?: boolean;
}

// Admin panel: fetches all users, lets you tweak role/staff flags in-place.
// The UI is intentionally minimal so the permission flow is easy to follow.
const AdminDashboard: React.FC = () => {
  const navigate = useNavigate();
  const { logout } = useAuth();
  const [users, setUsers] = useState<UserRow[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Grab the full user list (admin-only endpoint). Keep errors visible to the user.
  const fetchUsers = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await api.get('accounts/users/');
      setUsers(res.data as UserRow[]);
    } catch (e: any) {
      setError(e?.message || 'Failed to load users');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchUsers();
  }, []);

  // Light PATCH helper so each control can update a single user without a page reload.
  const updateUser = async (u: UserRow, updates: Partial<UserRow>) => {
    try {
      const res = await api.patch(`accounts/users/${u.id}/`, updates);
      setUsers((prev) => prev.map((row) => (row.id === u.id ? res.data : row)));
    } catch (e: any) {
      setError(e?.message || 'Failed to update user');
    }
  };

  return (
    <div className="dashboard-container admin-dashboard">
      <div className="dashboard-header">
        <h2 className="heading-xl">Admin Dashboard</h2>
        <button className="button" onClick={() => { logout(); navigate('/'); }}>Logout</button>
      </div>
      <p>Welcome, admin! Manage users and courses.</p>

      {error && <div className="auth-error">{error}</div>}
      {loading ? (
        <p>Loading users...</p>
      ) : (
        <table className="table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Username</th>
              <th>Email</th>
              <th>Role</th>
              <th>Staff</th>
              <th>Superuser</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {users.map((u) => (
              <tr key={u.id}>
                <td>{u.id}</td>
                <td>{u.username}</td>
                <td>{u.email || ''}</td>
                <td>
                  <select
                    aria-label={`Role for user ${u.username}`}
                    title={`Role for user ${u.username}`}
                    value={u.role || 'student'}
                    onChange={(e) => updateUser(u, { role: e.target.value as any })}
                  >
                    <option value="student">student</option>
                    <option value="teacher">teacher</option>
                    <option value="admin">admin</option>
                  </select>
                </td>
                <td>
                  <input
                    type="checkbox"
                    aria-label={`Staff flag for user ${u.username}`}
                    title={`Staff flag for user ${u.username}`}
                    checked={!!u.is_staff}
                    onChange={(e) => updateUser(u, { is_staff: e.target.checked })}
                  />
                </td>
                <td>
                  <input
                    type="checkbox"
                    aria-label={`Superuser flag for user ${u.username}`}
                    title={`Superuser flag for user ${u.username}`}
                    checked={!!u.is_superuser}
                    onChange={(e) => updateUser(u, { is_superuser: e.target.checked })}
                  />
                </td>
                <td>
                  <button
                    className="button"
                    onClick={() => updateUser(u, { role: 'student', is_staff: false, is_superuser: false })}
                  >
                    Demote to student
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
};

export default AdminDashboard;
