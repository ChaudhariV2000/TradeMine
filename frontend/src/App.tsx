import {
  Route,
  Routes,
} from "react-router-dom";

import { DashboardLayout } from "./layouts/DashboardLayout";
import {
  PaperTrading,
} from "./pages/PaperTrading";
import { Dashboard } from "./pages/Dashboard";
import { Portfolio } from "./pages/Portfolio";
import { Scanner } from "./pages/Scanner";
import { Research } from "./pages/Research";
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

        <Route
          path="scanner"
          element={<Scanner />}
        />
        <Route
        path="research"
        element={<Research />}
      />
      </Route>
      <Route
      path="paper-trading"
      element={<PaperTrading />}
    />
    </Routes>
  );
}

export default App;