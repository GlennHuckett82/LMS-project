import React from "react";
import { render, screen, waitFor, fireEvent } from "@testing-library/react";
import Profile from "./Profile";
import { AuthContext } from "../auth/AuthContext";
import api from "../services/api";

jest.mock("../services/api");

// Provide a minimal mock of react-router-dom so Link works in tests.
jest.mock("react-router-dom", () => {
  const React = require("react");
  return {
    Link: ({ children, to }: any) => <a href={typeof to === "string" ? to : "#"}>{children}</a>,
  };
});

const mockedGet = api.get as jest.MockedFunction<typeof api.get>;
const mockedPost = api.post as jest.MockedFunction<typeof api.post>;

describe("Profile page", () => {
  beforeEach(() => {
    jest.clearAllMocks();

    mockedGet.mockImplementation((url: string) => {
      if (url === "/courses/") {
        return Promise.resolve({
          data: [
            {
              id: 1,
              title: "Course A",
              description: "Desc A",
            },
          ],
        } as any);
      }
      if (url === "/enrollments/my-enrollments/") {
        return Promise.resolve({
          data: [
            {
              course: { id: 1 },
            },
          ],
        } as any);
      }
      if (url === "/lessons/") {
        return Promise.resolve({
          data: [
            {
              id: 10,
              title: "Lesson 1",
              is_completed: false,
              course: { id: 1 },
            },
          ],
        } as any);
      }
      return Promise.resolve({ data: [] } as any);
    });

    mockedPost.mockResolvedValue({ data: {} } as any);
  });

  it("renders courses and lessons for an enrolled user", async () => {
    const logout = jest.fn();

    render(
      <AuthContext.Provider
        value={{
          isAuthenticated: true,
          accessToken: "token",
          login: jest.fn(),
          logout,
        }}
      >
        <Profile />
      </AuthContext.Provider>
    );

    expect(await screen.findByText(/my profile/i)).toBeInTheDocument();
    expect(await screen.findByText("Course A")).toBeInTheDocument();

    const viewLessonsButton = await screen.findByRole("button", {
      name: /view lessons/i,
    });

    await waitFor(() => expect(viewLessonsButton).not.toBeDisabled());

    fireEvent.click(viewLessonsButton);

    expect(await screen.findByText("Lesson 1")).toBeInTheDocument();
  });
});
