import { QueryClient, QueryClientProvider } from "@tanstack/react-query"
import { Button } from "@/components/ui/button"
import Logo from "@/components/logo/logo"
import { Send } from "lucide-react"

const queryClient = new QueryClient()

function App() {
    return (
        <QueryClientProvider client={queryClient}>
            <div className="min-h-svh">
                <header className="w-full flex justify-center p-2 shadow">
                    <div className="w-60">
                        <Logo />
                    </div>
                </header>
                <main className="md:max-w-2xl m-auto">
                    <div className="w-full flex flex-col p-4">
                        <div className="animate-in fade-in duration-500 max-w-11/12 p-2 prose">
                            <p>Hello there!</p>
                            <p>How can I help you with Canvas today?</p>
                        </div>
                        <div className="animate-in fade-in duration-500 self-end max-w-11/12 md:max-w-1/2 p-2 px-6 text-white bg-rose-500 rounded-full shadow">
                            <p>I have a question about Canvas. How can add a page to my course?</p>
                        </div>
                        <div className="animate-in fade-in duration-500 max-w-11/12 p-2 prose">
                            <p>Here&#39;s how you can create week-by-week links in your Canvas course to guide students:</p>
                            <p><strong>Method 1: Linking to Modules</strong></p>
                            <p>This is the most common and straightforward approach:</p>
                            <ol>
                                <li><p><strong>Create a Module for Each Week:</strong> Organize your course content into modules, labeling each one clearly (e.g., &quot;&quot;Week 1: Introduction,&quot;&quot; &quot;&quot;Week 2: Research Methods&quot;&quot;).</p>
                                </li>
                                <li><p><strong>Create a &quot;&quot;Weekly Overview&quot;&quot; Page (or use your Course Home Page):</strong> This is the page where you&#39;ll provide the links.</p>
                                </li>
                                <li><p><strong>Add Links to Modules:</strong></p>
                                    <ul>
                                        <li><strong>Edit the page.</strong></li>
                                        <li><strong>Type the text you want to use as a link</strong> (e.g., &quot;&quot;Week 1,&quot;&quot; &quot;&quot;Begin Week 2&quot;&quot;).</li>
                                        <li><strong>Highlight the text.</strong></li>
                                        <li><strong>Use the Rich Content Editor:</strong> Look for the &quot;&quot;Links&quot;&quot; icon (it often looks like a chain). Click it.</li>
                                        <li><strong>Select &quot;&quot;Course Links&quot;&quot;:</strong> A sidebar will appear with different course elements.</li>
                                        <li><strong>Choose &quot;&quot;Modules&quot;&quot;:</strong> Expand the Modules section.</li>
                                        <li><strong>Select the appropriate module:</strong> Click the name of the module you want to link to. The highlighted text will now become a link to that module.</li>
                                        <li><strong>Repeat</strong> for each week.</li>
                                        <li><strong>Save the page.</strong></li>
                                    </ul>
                                </li>
                            </ol>
                            <p><strong>Method 2: Linking to Pages Within Modules</strong></p>
                            <p>If you want to provide a more detailed overview <em>before</em> students jump into the module content, you can create a page <em>within</em> each module:</p>
                            <ol>
                                <li><p><strong>Create a Module for Each Week</strong> (as above).</p>
                                </li>
                                <li><p><strong>Create a Page <em>within</em> each Module:</strong> This page will contain the overview of the week&#39;s activities, readings, and assignments. Give it a descriptive name (e.g., &quot;&quot;Week 1 Overview,&quot;&quot; &quot;&quot;Week 2 - What to Do This Week&quot;&quot;).  Make sure this page is published.</p>
                                </li>
                                <li><p><strong>Create a &quot;&quot;Weekly Overview&quot;&quot; Page (or use your Course Home Page):</strong> This is the page where you&#39;ll provide the links.</p>
                                </li>
                                <li><p><strong>Add Links to Pages:</strong></p>
                                    <ul>
                                        <li><strong>Edit the &quot;&quot;Weekly Overview&quot;&quot; page.</strong></li>
                                        <li><strong>Type the text you want to use as a link</strong> (e.g., &quot;&quot;Week 1,&quot;&quot; &quot;&quot;Begin Week 2&quot;&quot;).</li>
                                        <li><strong>Highlight the text.</strong></li>
                                        <li><strong>Use the Rich Content Editor:</strong> Look for the &quot;&quot;Links&quot;&quot; icon. Click it.</li>
                                        <li><strong>Select &quot;&quot;Course Links&quot;&quot;.</strong> A sidebar will appear with different course elements.</li>
                                        <li><strong>Choose &quot;&quot;Pages&quot;&quot;:</strong> Expand the Pages section.</li>
                                        <li><strong>Select the appropriate page:</strong> Click the name of the page you created within the module. The highlighted text will now become a link to that page.</li>
                                        <li><strong>Repeat</strong> for each week.</li>
                                        <li><strong>Save the page.</strong></li>
                                    </ul>
                                </li>
                            </ol>
                            <p><strong>Tips:</strong></p>
                            <ul>
                                <li><strong>Consistency:</strong> Use a consistent naming convention for your modules and pages.</li>
                                <li><strong>Clarity:</strong>  On your &quot;&quot;Weekly Overview&quot;&quot; page, provide brief descriptions of what students will find in each week&#39;s module/page.</li>
                                <li><strong>Buttons (Optional):</strong> Instead of plain text links, you can create button-style links using HTML or by inserting images and linking them. This can make the page more visually appealing.</li>
                                <li><strong>Student View:</strong> Always check your links in Student View to ensure they work correctly.</li>
                            </ul>
                        </div>
                    </div>
                    <div className="w-full flex flex-col gap-4">
                        <div className="w-full min-h-36 outline-rose-200 outline-2 shadow-inner rounded-md">
                        </div>
                        <div className="flex flex-col md:self-end md:min-w-24">
                            <Button><Send />Ask</Button>
                        </div>
                    </div>
                </main>
                <footer className="w-full p-4 flex flex-col items-center">
                    <p className="text-sm text-rose-300">CPAL is an AI-powered chatbot, so it may be wrong sometimes.</p>
                    <p className="text-sm text-rose-300">Be sure to verify all information with other sources.</p>
                    <br />
                    <p className="text-sm text-rose-300">
                        <span>Created by <a className="text-rose-500 underline" href="https://www.seanbeirnes.com" target="_blank">Sean Beirnes</a></span>
                        <span>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;</span>
                        <span><a className="text-rose-500 underline" href="https://github.com/seanbeirnes/cpal" target="_blank">View source code on GitHub</a></span></p>
                </footer>
            </div>
        </QueryClientProvider>
    )
}

export default App
