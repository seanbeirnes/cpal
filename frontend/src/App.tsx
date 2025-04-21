import { QueryClient, QueryClientProvider } from "@tanstack/react-query"
import Header from "./components/layout/header"
import ChatController from "./components/controller/chat-controller"

const queryClient = new QueryClient()

function App() {
    return (
        <QueryClientProvider client={queryClient}>
            <div className="min-h-svh">
                <Header />
                <main className="md:max-w-2xl m-auto">
                    <ChatController />
                </main>
            </div>
        </QueryClientProvider>
    )
}

export default App
