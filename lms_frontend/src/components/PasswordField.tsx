import React, { useState } from 'react';
import Eye from './icons/Eye';
import EyeOff from './icons/EyeOff';

export interface PasswordFieldProps {
  id: string;
  value: string;
  onChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
  name?: string;
  autoComplete?: string;
  disabled?: boolean;
  label?: string;
}

const PasswordField: React.FC<PasswordFieldProps> = ({
  id,
  value,
  onChange,
  name,
  autoComplete = 'current-password',
  disabled,
  label = 'Password',
}) => {
  const [show, setShow] = useState(false);

  return (
    <div className="auth-field password-field">
      <label className="auth-label" htmlFor={id}>{label}</label>
      <div className="password-input-wrap">
        <input
          className="auth-input"
          id={id}
          name={name}
          type={show ? 'text' : 'password'}
          value={value}
          onChange={onChange}
          autoComplete={autoComplete}
          disabled={disabled}
          aria-describedby={`${id}-desc`}
        />
        <button
          type="button"
          className="auth-toggle"
          aria-label={show ? 'Hide password' : 'Show password'}
          aria-controls={id}
          onClick={() => setShow((s) => !s)}
        >
          {show ? <EyeOff /> : <Eye />}
          <span id={`${id}-desc`} className="sr-only">{show ? 'Password is visible' : 'Password is hidden'}</span>
        </button>
      </div>
    </div>
  );
};

export default PasswordField;
