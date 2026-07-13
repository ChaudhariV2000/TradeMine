import {
  Route,
  Routes,
} from "react-router-dom";

import { DashboardLayout } from "./layouts/DashboardLayout";
import { Dashboard } from "./pages/Dashboard";
import { Portfolio } from "./pages/Portfolio";

import "./App.css";

function App() {
  return (
    <Routes>
      <Route
        element={
          <DashboardLayout />
        }
      >
        <Route
          index
          element={<Dashboard />}
        />

        <Route
          path="portfolio"
          element={<Portfolio />}
        />
      </Route>
    </Routes>
  );
}

export default App;