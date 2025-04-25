import App from "./App";

import { createRoot } from "react-dom/client";
import { Provider } from "react-redux";

import store from "./components/Redux/ReduxStore";

import "./index.css";

const container = document.getElementById("root");
const root = createRoot(container);
root.render(
  <Provider store={store}>
    <App />
  </Provider>
);
