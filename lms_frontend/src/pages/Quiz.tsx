import React, { useState, useEffect, useContext } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useAuth } from '../auth/AuthContext';
import axios from 'axios';
import './Quiz.css';

// Define TypeScript interfaces for our data structures
interface Choice {
    id: number;
    text: string;
}

interface Question {
    id: number;
    text: string;
    choices: Choice[];
}

interface Quiz {
    id: number;
    title: string;
    questions: Question[];
}

const QuizPage = () => {
    const { lessonId } = useParams<{ lessonId: string }>();
    const [quiz, setQuiz] = useState<Quiz | null>(null);
    const [selectedAnswers, setSelectedAnswers] = useState<{ [key: number]: number }>({});
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const { accessToken } = useAuth();
    const navigate = useNavigate();

    useEffect(() => {
        const fetchQuiz = async () => {
            try {
                const response = await axios.get(`http://localhost:8000/api/quizzes/${lessonId}/`, {
                    headers: {
                        'Authorization': `Bearer ${accessToken}`
                    }
                });
                setQuiz(response.data);
            } catch (err) {
                setError('Failed to load the quiz. Please try again later.');
                console.error(err);
            } finally {
                setIsLoading(false);
            }
        };

        fetchQuiz();
    }, [lessonId, accessToken]);

    const handleAnswerChange = (questionId: number, choiceId: number) => {
        setSelectedAnswers(prev => ({
            ...prev,
            [questionId]: choiceId
        }));
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (Object.keys(selectedAnswers).length !== quiz?.questions.length) {
            alert('Please answer all questions before submitting.');
            return;
        }

        const submissionData = {
            quiz: quiz?.id,
            answers: Object.entries(selectedAnswers).map(([questionId, choiceId]) => ({
                question: parseInt(questionId),
                selected_choice: choiceId
            }))
        };

        try {
            const response = await axios.post('http://localhost:8000/api/quizzes/attempt/', submissionData, {
                headers: {
                    'Authorization': `Bearer ${accessToken}`
                }
            });
            // The backend will create the attempt and return the new attempt's ID.
            // We need to implement the result page to redirect to.
            // For now, let's assume the attempt object is returned directly
            const attemptId = response.data.id;
            navigate(`/quiz/result/${attemptId}`);
        } catch (err: any) {
            if (err.response && err.response.data) {
                setError(err.response.data.detail || 'Failed to submit the quiz.');
            } else {
                setError('Failed to submit the quiz. Please check your connection.');
            }
            console.error(err);
        }
    };

    if (isLoading) return <div>Loading Quiz...</div>;
    if (error) return <div className="error-message">{error}</div>;
    if (!quiz) return <div>No quiz found for this lesson.</div>;

    return (
        <div className="quiz-container">
            <h1>{quiz.title}</h1>
            <form onSubmit={handleSubmit}>
                {quiz.questions.map((question, index) => (
                    <div key={question.id} className="question-block">
                        <h3>Question {index + 1}</h3>
                        <p>{question.text}</p>
                        <div className="choices-group">
                            {question.choices.map(choice => (
                                <label key={choice.id} className="choice-label">
                                    <input
                                        type="radio"
                                        name={`question-${question.id}`}
                                        value={choice.id}
                                        onChange={() => handleAnswerChange(question.id, choice.id)}
                                        checked={selectedAnswers[question.id] === choice.id}
                                    />
                                    {choice.text}
                                </label>
                            ))}
                        </div>
                    </div>
                ))}
                <button type="submit" className="submit-button">Submit Quiz</button>
            </form>
        </div>
    );
};

export default QuizPage;
