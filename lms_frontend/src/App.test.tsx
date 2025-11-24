
// Basic smoke test for the App component using React Testing Library.
// Verifies that the "learn react" link is rendered on initial load.
import React from 'react';
import { render, screen } from '@testing-library/react';
import App from './App';


test('renders learn react link', () => {
  // Render the App component
  render(<App />);
  // Find the link with text "learn react" (case-insensitive)
  const linkElement = screen.getByText(/learn react/i);
  // Assert that the link is present in the document
  expect(linkElement).toBeInTheDocument();
});
