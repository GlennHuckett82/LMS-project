import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import api from '../services/api';
import './Quiz.css'; // Reusing the same CSS file

// Define TypeScript interfaces for the result data
interface CorrectChoice {
    id: number;
    text: string;
}

interface QuestionResult {
    id: number;
    text: string;
    explanation: string;
    choices: { id: number; text: string }[];
    correct_choice: CorrectChoice;
}

interface AnswerResult {
    question: QuestionResult;
    selected_choice: number;
}

interface QuizResultData {
    id: number;
    quiz_title: string;
    score: number;
    completed_at: string;
    answers: AnswerResult[];
}

// Quiz result page: fetches the attempt by id and shows score plus explanations for any misses.
const QuizResultPage = () => {
    const { attemptId } = useParams<{ attemptId: string }>();
    const [result, setResult] = useState<QuizResultData | null>(null);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        // Retrieve the graded attempt as soon as we know the attempt id.
        const fetchResult = async () => {
            try {
                const response = await api.get(`/quizzes/result/${attemptId}/`);
                setResult(response.data);
            } catch (err) {
                setError('Failed to load quiz results.');
                console.error(err);
            } finally {
                setIsLoading(false);
            }
        };

        fetchResult();
    }, [attemptId]);

    if (isLoading) return <div>Loading Results...</div>;
    if (error) return <div className="error-message">{error}</div>;
    if (!result) return <div>Could not find results for this attempt.</div>;

    return (
        <div className="quiz-container">
            <h1>{result.quiz_title} - Results</h1>
            <div className="quiz-score">
                <h2>Your Score: {result.score.toFixed(2)}%</h2>
            </div>
            <p>Completed on: {new Date(result.completed_at).toLocaleString()}</p>

            {result.answers.map((answer, index) => {
                const question = answer.question;
                const userChoice = question.choices.find(c => c.id === answer.selected_choice);
                const isCorrect = userChoice?.id === question.correct_choice.id;

                return (
                    <div key={question.id} className={`question-block result ${isCorrect ? 'correct' : 'incorrect'}`}>
                        <h3>Question {index + 1}: {isCorrect ? 'Correct' : 'Incorrect'}</h3>
                        <p>{question.text}</p>
                        <div className="choices-group">
                            <p><strong>Your answer:</strong> {userChoice?.text || 'Not answered'}</p>
                            {!isCorrect && (
                                <>
                                    <p><strong>Correct answer:</strong> {question.correct_choice.text}</p>
                                    <p className="explanation"><strong>Explanation:</strong> {question.explanation}</p>
                                </>
                            )}
                        </div>
                    </div>
                );
            })}

            <div className="quiz-navigation">
                <Link to="/profile" className="nav-button">
                    &larr; Back to Profile
                </Link>
            </div>
        </div>
    );
};

export default QuizResultPage;
