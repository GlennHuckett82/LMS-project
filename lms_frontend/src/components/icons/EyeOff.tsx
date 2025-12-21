import React from 'react';

interface Props {
  size?: number;
  className?: string;
}

const EyeOff: React.FC<Props> = ({ size = 20, className }) => (
  <svg
    xmlns="http://www.w3.org/2000/svg"
    width={size}
    height={size}
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    strokeWidth="2"
    strokeLinecap="round"
    strokeLinejoin="round"
    className={className}
    aria-hidden="true"
    focusable="false"
  >
    {/* Eye outline */}
    <path d="M1 12 C5 5 19 5 23 12 C19 19 5 19 1 12 Z" />
    {/* Pupil */}
    <circle cx="12" cy="12" r="3" />
    {/* Strike-through to indicate hidden */}
    <line x1="3" y1="3" x2="21" y2="21" />
  </svg>
);

export default EyeOff;
