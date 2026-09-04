import { useState } from 'react';
import { X } from 'lucide-react';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { oneDark } from 'react-syntax-highlighter/dist/esm/styles/prism';
import useStore from '../store/useStore';
import { approveAgent, fetchFiles } from '../api/client';

export default function ReviewDialog() {
  const {
    pendingReview, setPendingReview,
    threadId, setAgentStatus,
  } = useStore();

  const [feedback, setFeedback] = useState('');
  const [rejecting, setRejecting] = useState(false);

  if (!pendingReview) return null;

  const handleDecision = (decision: 'approve' | 'reject') => {
    setPendingReview(null);
    setAgentStatus(decision === 'approve' ? 'applying' : 'coding');
    setRejecting(false);
    setFeedback('');

    approveAgent(threadId, decision, decision === 'reject' ? feedback : '', (event: Record<string, any>) => {
      switch (event.type) {
        case 'status':
          if (event.status === 'done' || event.status === 'tested') {
            setAgentStatus('done');
            fetchFiles().then((data) => {
              const files = Array.isArray(data) ? data : data.files || [];
              useStore.getState().setFiles(files);
            });
          } else {
            setAgentStatus(event.status);
          }
          break;
        case 'done':
          setAgentStatus('done');
          fetchFiles().then((data) => {
            const files = Array.isArray(data) ? data : data.files || [];
            useStore.getState().setFiles(files);
          });
          break;
        case 'approval_needed':
          setPendingReview({
            threadId,
            plan: event.plan || '',
            reviewResult: event.review_result || '',
            testOutput: event.test_output || '',
            changes: event.changes || [],
          });
          setAgentStatus('waiting_approval');
          break;
        case 'test':
          useStore.getState().setTestOutput(`${event.status === 'tests_passed' || event.status === 'done' ? 'PASS' : 'FAIL'}\n${event.output || ''}`);
          break;
        case 'error':
          setAgentStatus('error');
          break;
      }
    });
  };

  const langFromPath = (filepath: string): string => {
    const ext = filepath.split('.').pop() || '';
    const map: Record<string, string> = {
      ts: 'typescript', tsx: 'tsx', js: 'javascript', jsx: 'jsx',
      py: 'python', json: 'json', css: 'css', html: 'html', md: 'markdown',
    };
    return map[ext] || 'text';
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60">
      <div className="bg-orion-bg-secondary rounded-lg border border-orion-border max-w-2xl w-full mx-4 max-h-[80vh] flex flex-col">
        {/* Header */}
        <div className="flex items-center justify-between px-6 py-4 border-b border-orion-border flex-shrink-0">
          <h2 className="text-lg font-semibold text-white">Review Changes</h2>
          <button
            onClick={() => setPendingReview(null)}
            className="p-1 rounded hover:bg-orion-bg-input text-orion-text-secondary hover:text-orion-text-primary transition-colors"
          >
            <X size={18} />
          </button>
        </div>

        {/* Content */}
        <div className="flex-1 overflow-y-auto p-6 space-y-4">
          {/* Plan Summary */}
          {pendingReview.plan && (
            <div className="bg-orion-accent-soft border border-orion-border rounded-lg p-4">
              <h3 className="text-xs font-semibold text-orion-accent-purple-hover uppercase tracking-wider mb-2">
                Plan Summary
              </h3>
              <p className="text-sm text-orion-text-primary whitespace-pre-wrap">
                {pendingReview.plan}
              </p>
            </div>
          )}

          {/* Review Result */}
          {pendingReview.reviewResult && (
            <div className="bg-orion-bg-tertiary border border-orion-border rounded-lg p-4">
              <h3 className="text-xs font-semibold text-orion-accent-purple-hover uppercase tracking-wider mb-2">
                AI Review
              </h3>
              <p className="text-sm text-orion-text-primary whitespace-pre-wrap">
                {pendingReview.reviewResult}
              </p>
            </div>
          )}

          {pendingReview.testOutput && (
            <div className="bg-orion-bg-tertiary border border-orion-border rounded-md p-4">
              <h3 className="text-xs font-semibold text-orion-text-secondary uppercase tracking-wider mb-2">Tests</h3>
              <pre className="text-[11px] font-mono text-orion-text-primary whitespace-pre-wrap max-h-40 overflow-auto">{pendingReview.testOutput}</pre>
            </div>
          )}

          {/* Changes */}
          {pendingReview.changes?.map((change: any, i: number) => (
            <div key={i} className="border border-orion-border rounded-lg overflow-hidden">
              <div className="px-4 py-2 bg-orion-bg-tertiary flex items-center justify-between">
                <span className="text-sm font-mono text-orion-accent-teal">{change.filepath}</span>
                <span className="text-xs text-orion-text-secondary">{change.explanation}</span>
              </div>
              {change.preview && (
                <SyntaxHighlighter
                  style={oneDark}
                  language={langFromPath(change.filepath)}
                  customStyle={{ margin: 0, borderRadius: 0, fontSize: '12px', maxHeight: '300px' }}
                >
                  {change.preview}
                </SyntaxHighlighter>
              )}
            </div>
          ))}
        </div>

        {/* Footer */}
        <div className="px-6 py-4 border-t border-orion-border flex-shrink-0 space-y-3">
          {rejecting && (
            <label className="block text-[11px] text-orion-text-secondary">
              Why? The coder gets this verbatim.
              <textarea
                value={feedback}
                onChange={(e) => setFeedback(e.target.value)}
                rows={3}
                className="mt-1 w-full bg-orion-bg-input border border-orion-border rounded-md px-3 py-2 text-sm text-orion-text-primary resize-none focus:outline-none focus:ring-2 focus:ring-orion-accent-purple"
              />
            </label>
          )}
          <div className="flex items-center justify-end gap-3">
            {rejecting ? (
              <button
                onClick={() => handleDecision('reject')}
                disabled={!feedback.trim()}
                className="h-10 px-4 rounded-md text-sm font-semibold text-orion-accent-red border border-orion-border hover:bg-orion-bg-tertiary disabled:opacity-40 focus:outline-none focus:ring-2 focus:ring-orion-accent-purple"
              >
                Send back with feedback
              </button>
            ) : (
              <button
                onClick={() => setRejecting(true)}
                className="h-10 px-4 rounded-md text-sm font-semibold text-orion-accent-red hover:bg-orion-bg-tertiary focus:outline-none focus:ring-2 focus:ring-orion-accent-purple"
              >
                Reject
              </button>
            )}
            <button
              onClick={() => handleDecision('approve')}
              className="h-10 px-4 rounded-md text-sm font-semibold bg-orion-accent-purple text-orion-text-primary hover:bg-orion-accent-purple-hover focus:outline-none focus:ring-2 focus:ring-orion-accent-purple focus:ring-offset-2 focus:ring-offset-orion-bg-secondary"
            >
              Approve and apply
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
