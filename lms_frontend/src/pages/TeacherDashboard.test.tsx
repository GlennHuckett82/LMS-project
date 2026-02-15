import React from "react";
import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import TeacherDashboard from "./TeacherDashboard";
import { AuthContext } from "../auth/AuthContext";
import api from "../services/api";

jest.mock("../services/api");

const mockedGet = api.get as jest.MockedFunction<typeof api.get>;
const mockedPost = api.post as jest.MockedFunction<typeof api.post>;
const mockedPatch = api.patch as jest.MockedFunction<typeof api.patch>;
const mockedDelete = api.delete as jest.MockedFunction<typeof api.delete>;

const mockedNavigate = jest.fn();

// Lightweight mock of react-router-dom so useNavigate works without a real router.
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
      value={{ isAuthenticated: true, accessToken: "token", login, logout }}
    >
      <TeacherDashboard />
    </AuthContext.Provider>
  );

  return { login, logout };
}

describe("TeacherDashboard", () => {
  beforeEach(() => {
    jest.clearAllMocks();

    // Default: one existing course owned by the teacher.
    mockedGet.mockImplementation((url: string) => {
      if (url === "courses/my/") {
        return Promise.resolve({
          data: [
            {
              id: 1,
              title: "Course A",
              description: "Desc A",
              created_at: "2025-01-01",
            },
          ],
        } as any);
      }
      return Promise.resolve({ data: [] } as any);
    });

    mockedPost.mockResolvedValue({
      data: {
        id: 2,
        title: "New Course",
        description: "",
        created_at: "2025-01-02",
      },
    } as any);

    mockedPatch.mockResolvedValue({
      data: {
        id: 1,
        title: "Updated Course",
        description: "Updated",
        created_at: "2025-01-01",
      },
    } as any);

    mockedDelete.mockResolvedValue({ data: {} } as any);
  });

  it("shows the teacher's courses with edit and delete actions", async () => {
    renderWithAuth();

    expect(await screen.findByText("Course A")).toBeInTheDocument();

    expect(
      screen.getByRole("button", { name: /edit course/i })
    ).toBeInTheDocument();
    expect(
      screen.getByRole("button", { name: /delete course/i })
    ).toBeInTheDocument();
  });

  it("creates a course when the Create button is clicked", async () => {
    renderWithAuth();

    const titleInput = screen.getByLabelText(/course title/i);
    fireEvent.change(titleInput, { target: { value: "My New Course" } });

    const createButton = screen.getByRole("button", { name: /create course/i });
    fireEvent.click(createButton);

    await waitFor(() => {
      expect(mockedPost).toHaveBeenCalled();
      const [calledUrl] = mockedPost.mock.calls[0];
      expect(calledUrl).toBe("courses/");
    });
  });

  it("allows editing an existing course title", async () => {
    renderWithAuth();

    const editButton = await screen.findByRole("button", { name: /edit course/i });
    fireEvent.click(editButton);

    const editTitleInput = await screen.findByLabelText(/edit course title/i);
    fireEvent.change(editTitleInput, { target: { value: "Updated Course" } });

    const saveButton = screen.getByRole("button", { name: /save/i });
    fireEvent.click(saveButton);

    await waitFor(() => {
      expect(mockedPatch).toHaveBeenCalled();
      const [calledUrl, body] = mockedPatch.mock.calls[0];
      expect(calledUrl).toBe("courses/1/");
      expect(body).toMatchObject({ title: "Updated Course" });
    });
  });
});
