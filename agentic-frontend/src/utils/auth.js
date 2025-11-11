// Save JWT token
export const saveToken = (token) => {
  localStorage.setItem("token", token);
};

// Get JWT token
export const getToken = () => {
  return localStorage.getItem("token");
};

// Remove token (logout)
export const removeToken = () => {
  localStorage.removeItem("token");
};
