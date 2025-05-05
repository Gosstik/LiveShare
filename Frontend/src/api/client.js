import Cookies from "js-cookie";
import { ENV } from "../config";

// import { toast } from 'react-toastify'; // Or your preferred notification library

const handleNetworkError = (taskName) => (error) => {
  console.log(`%cAPI call '${taskName}' failed: network error`, "color: red");
  Promise.reject(error);
};

const getResponseWithApiErrorHandling = (taskName) => async (response) => {
  if (response.ok) {
    return response.json();
  }

  const body = await response.json();

  console.groupCollapsed(
    `%cGET ${response.url} [${response.status}]`,
    "color: red"
  );

  console.log(`Task: ${taskName}`);
  console.log(`Status: ${response.status}`);
  console.log(`Date: ${new Date(Date.now()).toISOString()}`);
  console.log("response:", response);
  console.log("body:", body);

  console.groupEnd();

  return body;
};

////////////////////////////////////////////////////////////////////////////////

// Clients
