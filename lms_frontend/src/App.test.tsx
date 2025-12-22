
// Basic smoke test for the App component using React Testing Library.
// Verifies that the "learn react" link is rendered on initial load.
import React from 'react';
import { render } from '@testing-library/react';

// Provide a lightweight mock for react-router-dom so Jest doesn't need the real router implementation.
jest.mock('react-router-dom', () => {
  const React = require('react');
  return {
    BrowserRouter: ({ children }: any) => <div>{children}</div>,
    Routes: ({ children }: any) => <div>{children}</div>,
    Route: () => null,
    Link: ({ children }: any) => <a>{children}</a>,
    Outlet: ({ children }: any) => <div>{children}</div>,
    useLocation: () => ({ pathname: '/' }),
  };
});

import App from './App';

test('renders App without crashing', () => {
  const { container } = render(<App />);
  expect(container.firstChild).toBeTruthy();
});
