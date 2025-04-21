import { LoaderCircle, Send } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { useState } from "react";

interface ChatComposerControllerProps {
    callback: Function
    disabled: boolean
}

function ChatComposerController(props: ChatComposerControllerProps) {
    const [text, useText] = useState("")

    const handleTextAreaUpdate = (event: React.ChangeEvent<HTMLTextAreaElement>) => {
        useText(event.target.value)
    }

    const handleButtonClick = () => {
        if (text.trim().length === 0) {
            return
        }
        const tmp: string = text
        useText("")
        props.callback(tmp)
    }

    const handleKeyPress = (event: React.KeyboardEvent<HTMLTextAreaElement>) => {
        if (event.key === "Enter" && text.trim().length > 0) {
            handleButtonClick()
        }
    }

    return (
        <>
            <Textarea disabled={props.disabled} onChange={handleTextAreaUpdate} onKeyDown={handleKeyPress} value={props.disabled ? "Processing your question..." : text} className="resize-none" placeholder="Ask your question...">
            </Textarea>
            <div className="flex flex-col md:self-end md:min-w-24">
                {props.disabled ? (
                    <Button disabled={true}><LoaderCircle className="animate-spin" /></Button>
                ) : (
                    <Button disabled={text.trim().length === 0}onClick={handleButtonClick}><Send />Ask</Button>
                )}
            </div>
        </>
    )
}

export default ChatComposerController
