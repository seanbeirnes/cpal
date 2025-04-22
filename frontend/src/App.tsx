import { createContext } from "react"
import { LoaderCircle } from "lucide-react"
import axios from "axios"
import { useQuery } from "@tanstack/react-query"
import Header from "./components/layout/header"
import ChatController from "./components/controller/chat-controller"

export interface AppConfig {
    captcha: string
}

export const ConfigContext = createContext<AppConfig | undefined>(undefined)

const fetchConfig = async () => {
    return await axios.get<AppConfig>("/api/config")
}

function App() {
    const { data, isLoading, isError, error } = useQuery({
        queryKey: ["app-config"],
        queryFn: fetchConfig
    })

    if (isError) {
        console.error(error)
        return (
            <div className="min-h-svh">
                <Header />
                <main className="md:max-w-2xl m-auto">
                    <p>Sorry... Service is unavailable right now</p>
                </main>
            </div>
        )
    }

    if (isLoading || !data) {
        return (
            <div className="min-h-svh">
                <Header />
                <main className="md:max-w-2xl m-auto">
                    <LoaderCircle className="text-rose-200 animate-spin" />
                </main>
            </div>
        )
    }

    return (
        <div className="min-h-svh">
            <script async src={`https://www.google.com/recaptcha/api.js?render=${data.data.captcha}`}></script>
            <ConfigContext.Provider value={data.data}>
                <Header />
                <main className="md:max-w-2xl m-auto">
                    <ChatController />
                </main>
            </ConfigContext.Provider>
        </div>
    )
}

export default App
