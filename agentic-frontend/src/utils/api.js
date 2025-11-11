import axios from "axios";

const API = axios.create({
  baseURL: "http://127.0.0.1:8000",
});

export const registerUser = async (data) => {
  const res = await API.post("/auth/register", data);
  return res.data;
};

export const loginUser = async (data) => {
  const res = await API.post("/auth/login", data);
  return res.data;
};

export const addReminder = async (data) => {
  const res = await API.post("/reminder/add", data);
  return res.data;
};

export const getReminders = async () => {
  const res = await API.get("/reminder/list");
  return res.data;
};

export const askAI = async (query) => {
  const res = await API.post("/ai/ask", { query });
  return res.data;
};
