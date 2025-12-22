// jest-dom adds custom jest matchers for asserting on DOM nodes.
// allows you to do things like:
// expect(element).toHaveTextContent(/react/i)
// learn more: https://github.com/testing-library/jest-dom
import '@testing-library/jest-dom';

// Provide a Jest-friendly mock for axios so tests don't try to load the ESM build.
jest.mock('axios', () => {
	const mockInstance = {
		interceptors: {
			request: { use: jest.fn() },
			response: { use: jest.fn() },
		},
		get: jest.fn(),
		post: jest.fn(),
	};
	const mockAxios = {
		create: jest.fn(() => mockInstance),
		// mimic axios.isAxiosError behaviour for objects that have a response property
		isAxiosError: jest.fn((err: any) => !!(err && (err as any).response)),
		...mockInstance,
	};
	return {
		__esModule: true,
		default: mockAxios,
	};
});
