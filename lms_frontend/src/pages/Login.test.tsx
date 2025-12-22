import React from "react";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import Login from "./Login";
import { AuthContext } from "../auth/AuthContext";
import { loginUser, fetchMe } from "../services/auth";

jest.mock("../services/auth");

const mockedLoginUser = loginUser as jest.MockedFunction<typeof loginUser>;
const mockedFetchMe = fetchMe as jest.MockedFunction<typeof fetchMe>;

const mockedNavigate = jest.fn();

// Lightweight mock of react-router-dom so tests don't depend on browser history.
jest.mock("react-router-dom", () => {
  const React = require("react");
  return {
    useNavigate: () => mockedNavigate,
  };
});

function renderWithAuth() {
  const login = jest.fn();
  const logout = jest.fn();

  render(
    <AuthContext.Provider
      value={{ isAuthenticated: false, accessToken: null, login, logout }}
    >
      <Login />
    </AuthContext.Provider>
  );

  return { login, logout };
}

describe("Login page", () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  it("renders username, password and submit button", () => {
    renderWithAuth();

    expect(screen.getByLabelText(/username/i)).toBeInTheDocument();
    expect(
      screen.getByLabelText(/password/i, { selector: "input" })
    ).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /login/i })).toBeInTheDocument();
  });

  it("logs in successfully and navigates based on role", async () => {
    mockedLoginUser.mockResolvedValue({
      access: "access-token",
      refresh: "refresh-token",
    } as any);
    mockedFetchMe.mockResolvedValue({
      id: 1,
      username: "teach",
      role: "teacher",
      is_staff: false,
      is_superuser: false,
    } as any);

    const { login } = renderWithAuth();

    fireEvent.change(screen.getByLabelText(/username/i), {
      target: { value: "teach" },
    });
    fireEvent.change(screen.getByLabelText(/password/i, { selector: "input" }), {
      target: { value: "secret" },
    });

    fireEvent.click(screen.getByRole("button", { name: /login/i }));

    await waitFor(() => {
      expect(mockedLoginUser).toHaveBeenCalledWith({
        username: "teach",
        password: "secret",
      });
      expect(login).toHaveBeenCalledWith("access-token", "refresh-token");
      expect(mockedFetchMe).toHaveBeenCalled();
      expect(mockedNavigate).toHaveBeenCalledWith("/teacher-dashboard");
    });
  });

  it("shows an error message when login fails", async () => {
    mockedLoginUser.mockRejectedValue({
      response: { data: { detail: "Invalid credentials" } },
    } as any);

    renderWithAuth();

    fireEvent.change(screen.getByLabelText(/username/i), {
      target: { value: "baduser" },
    });
    fireEvent.change(screen.getByLabelText(/password/i, { selector: "input" }), {
      target: { value: "badpass" },
    });

    fireEvent.click(screen.getByRole("button", { name: /login/i }));

    expect(
      await screen.findByText(/invalid credentials/i)
    ).toBeInTheDocument();
  });
});
