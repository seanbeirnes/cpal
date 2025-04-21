import MarkdownRenderer from "@/components/render/markdown-renderer"

interface AnswerSource {
    url: string
    title: string
    score: number
}

export interface AnswerResponse {
    answer: string
    sources: AnswerSource[]
}

interface AnswerChatProps {
    answer: AnswerResponse
}

export function AnswerChat(props: AnswerChatProps){
    return (
                <div className="animate-in fade-in duration-500 max-w-11/12 p-2">
                    <MarkdownRenderer markdown={props.answer.answer} />
                    {props.answer.sources.length > 0 &&
                        <section className="w-full prose">
                            <hr />
                            <h2>Sources</h2>
                            <p>Consider checking the following {props.answer.sources.length > 1 ? "links" : "link"} for more information:</p>
                            <ul>
                                {props.answer.sources.sort((a, b) => b.score - a.score).map((source: AnswerSource, index: number) => {
                                    return (
                                        <li key={`${index}-${source.score}`}><a className="text-sm text-rose-500 underline" href={source.url} target="_blank">{source.title}</a></li>
                                    )
                                })}
                            </ul>
                        </section>
                    }
                </div>
    )
}
