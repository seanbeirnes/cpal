import ReactMarkdown from 'react-markdown'
import rehypeRaw from 'rehype-raw'
import rehypeSanitize from 'rehype-sanitize'

interface MarkdownRendererProps {
    markdown?: string;
    className?: string;
}

function MarkdownRenderer(props: MarkdownRendererProps) {
    return (
        <div className={props.className + " prose"}>
            <ReactMarkdown rehypePlugins={[rehypeRaw, rehypeSanitize]}>
                {props.markdown}
            </ReactMarkdown>
        </div>
    )
}

export default MarkdownRenderer
