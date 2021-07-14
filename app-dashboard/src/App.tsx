import { useDisclosure } from "@chakra-ui/hooks";
import { Flex, Text } from "@chakra-ui/layout";
import { Collapse } from "@chakra-ui/transition";
import { useEffect, useState } from "react";
import { QueryClient, QueryClientProvider } from "react-query";
import { BrowserRouter as Router, Switch, Route } from "react-router-dom";
import "./App.css";
import NotifPortal from "./components/NotifPortal";
import Dashboard from "./pages/Dashboard";
import Login from "./pages/Login";
import Templates from "./pages/Templates";

function App() {
  const { isOpen, onOpen, onClose } = useDisclosure();
  const [networkToggle, setNetworkToggle] = useState<string | null>(null);
  const queryClient = new QueryClient();

  useEffect(() => {
    const online: any = window.addEventListener("online", () => {
      onClose();
      onOpen();
      setNetworkToggle("online");
      setTimeout(() => {
        onClose();
      }, 4000);
    });
    const offline: any = window.addEventListener("offline", () => {
      onOpen();
      setNetworkToggle("offline");
    });

    return () => {
      try {
        window.removeEventListener("online", online);
        window.removeEventListener("offline", offline);
      } catch (e) {}
    };
  }, []);

  return (
    <QueryClientProvider client={queryClient}>
      <NotifPortal el="networkstatus">
        <Collapse in={isOpen} animateOpacity>
          {networkToggle == "online" ? (
            <Flex align="center" justify="center" bg="#0dc445" w="100%">
              <Text color="white" fontSize="sm" p="1">
                Your network is restored
              </Text>
            </Flex>
          ) : (
            <Flex align="center" justify="center" bg="#f51b1b" w="100%">
              <Text color="white" fontSize="sm" p="1">
                You're on offline mode
              </Text>
            </Flex>
          )}
        </Collapse>
      </NotifPortal>
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
