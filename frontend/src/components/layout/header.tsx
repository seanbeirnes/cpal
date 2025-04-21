import Logo from "../logo/logo"

function Header() {
    return (
        <header className="w-full flex justify-center p-2 bg-white shadow">
            <div className="w-60">
                <a href={window.location.href}><Logo /></a>
            </div>
        </header>
    )
}

export default Header
