import axios from 'axios';

/**
 * The API endpoint for user authentication.
 * Assumes a reverse proxy is configured (e.g., in vite.config.ts)
 * to forward requests from '/auth/login' to the backend server.
 */
const API_URL = '/auth/login';
const REGISTER_URL = '/auth/register';

/**
 * Defines the expected shape of the successful login response payload,
 * which should contain a JSON Web Token (JWT).
 */
interface LoginResponse {
  access_token: string;
}

/**
 * Asynchronously logs in a user by sending credentials to the backend.
 *
 * @param {string} username The user's username.
 * @param {string} password The user's password.
 * @returns {Promise<boolean>} A promise that resolves to 'true' on success.
 * @throws {Error} Throws an error on login failure (e.g., wrong credentials).
 */
const login = async (username: string, password: string): Promise<boolean> => {
  try {
    // 1. Send credentials to the backend API endpoint.
    const response = await axios.post<LoginResponse>(API_URL, {
      username,
      password,
    });

    // 2. On a successful response, extract and store the JWT.
    if (response.data.access_token) {
      // 3. Store the token in localStorage for session persistence.
      localStorage.setItem('user_token', response.data.access_token);
      return true;
    }
    return false;

  } catch (err) {
    // 4. Handle network errors or 401 (Unauthorized) responses.
    console.error('Login failed:', err);
    throw new Error('Invalid username or password.');
  }
};

/**
 * Registers a new user by sending credentials to the backend.
 *
 * @param {string} username The user's username.
 * @param {string} password The user's password.
 * @returns {Promise<boolean>} A promise that resolves to 'true' on success.
 * @throws {Error} Throws an error on registration failure.
 */
const register = async (username: string, password: string): Promise<boolean> => {
  try {
    await axios.post(REGISTER_URL, { username, password });
    return true;
  } catch (err) {
    console.error('Registration failed:', err);
    throw new Error('Registration failed. Username might be taken.');
  }
};

/**
 * Logs out the current user.
 * This function clears the session token from localStorage and
 * forces a redirect to the login page, effectively resetting the session.
 */
const logout = () => {
  localStorage.removeItem('user_token');
  // Redirect to the login page to ensure a clean state.
  window.location.href = '/login';
};

/**
 * Retrieves the current user's authentication token.
 *
 * @returns {string | null} The JWT string if it exists, or 'null'.
 */
const getCurrentUserToken = (): string | null => {
  return localStorage.getItem('user_token');
};

/**
 * Encapsulates the authentication functions into a single service object.
 */
const authService = {
  login,
  register,
  logout,
  getCurrentUserToken,
};

// Exports the service for use across the application.
export default authService;