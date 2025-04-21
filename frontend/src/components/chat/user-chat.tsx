interface UserChatProps {
    message: string
}

function UserChat(props: UserChatProps) {
    return (
        <div className="animate-in fade-in duration-500 self-end max-w-11/12 md:max-w-1/2 p-2 px-6 text-white bg-rose-500 rounded-3xl shadow-md">
            <p>{props.message}</p>
        </div>
    )
}

export default UserChat
