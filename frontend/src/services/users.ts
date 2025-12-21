import { api } from "./api";

export async function getUsers() {
  const response = await api.get("/users");
  return response.data;
}
