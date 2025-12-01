import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import api from '../services/api';
import { markLessonComplete } from '../services/auth';
import '../App.css';

interface Lesson {
  id: number;
  title: string;
  content: string;
  is_completed: boolean;
}

const LessonDetail: React.FC = () => {
  const { lessonId } = useParams<{ lessonId: string }>();
  const [lesson, setLesson] = useState<Lesson | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isCompleted, setIsCompleted] = useState(false);
  const [completionMessage, setCompletionMessage] = useState<string>('');

  useEffect(() => {
    const fetchLesson = async () => {
      try {
        // The backend expects the lesson detail endpoint to be nested under courses.
        // The correct endpoint is /api/lessons/{id}/ which is handled by the LessonViewSet.
        // The previous assumption about nesting was incorrect.
        const response = await api.get<Lesson>(`/lessons/${lessonId}/`);
        setLesson(response.data);
        setIsCompleted(response.data.is_completed);
      } catch (err: any) {
        setError(err.message || 'Failed to fetch lesson details.');
      } finally {
        setLoading(false);
      }
    };

    fetchLesson();
  }, [lessonId]);

  const handleMarkComplete = async () => {
    if (!lesson) return;

    try {
      await markLessonComplete(lesson.id);
      setIsCompleted(true);
      setCompletionMessage('Lesson marked as complete! You can now return to your profile.');
    } catch (err: any) {
      setError(err.message || 'Failed to mark lesson as complete.');
    }
  };

  if (loading) return <p className="loading-message">Loading lesson...</p>;
  if (error) return <p className="error-message">{error}</p>;
  if (!lesson) return <p>Lesson not found.</p>;

  return (
    <div className="lesson-detail-container">
      <h1 className="lesson-title">{lesson.title}</h1>
      <div
        className="lesson-content"
        dangerouslySetInnerHTML={{ __html: lesson.content }}
      />

      <div className="lesson-actions">
        {isCompleted ? (
          <p className="completion-status">✓ You have completed this lesson.</p>
        ) : (
          <button
            onClick={handleMarkComplete}
            className="auth-button"
            disabled={isCompleted}
          >
            Mark as Complete
          </button>
        )}
        {completionMessage && <p className="completion-message">{completionMessage}</p>}
      </div>

      <div className="navigation-links">
        <Link to="/profile" className="nav-link">
          &larr; Back to Profile
        </Link>
      </div>
    </div>
  );
};

export default LessonDetail;