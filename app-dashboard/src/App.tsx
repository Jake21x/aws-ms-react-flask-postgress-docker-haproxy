import { QueryClient, QueryClientProvider } from "react-query";
import { BrowserRouter as Router, Switch, Route } from "react-router-dom";
import "./App.css";
import Dashboard from "./pages/Dashboard";
import Login from "./pages/Login";
import Templates from "./pages/Templates";

function App() {
  const queryClient = new QueryClient();

  return (
    <QueryClientProvider client={queryClient}>
      <Router>
        <Switch>
          <Route path="/admin/templates" component={Templates} />
          <Route path="/login" component={Login} />
          <Route exact path="/" component={Dashboard} />
        </Switch>
      </Router>
    </QueryClientProvider>
  );
}

export default App;
