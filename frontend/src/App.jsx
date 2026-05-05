import { useEffect, useMemo, useRef, useState } from 'react';
import { createGameboard } from './api/client';

const CATEGORY_ORDER = ['movies', 'tv', 'music', 'celebrities', 'sports'];
const VALUES = [200, 400, 600, 800, 1000];

function normalizeText(value) {
  return String(value ?? '')
    .toLowerCase()
    .replace(/[^a-z0-9\s]/g, ' ')
    .replace(/\b(the|a|an|who is|what is|whats|whos)\b/g, ' ')
    .replace(/\s+/g, ' ')
    .trim();
}

function levenshtein(left, right) {
  if (left === right) return 0;
  if (!left.length) return right.length;
  if (!right.length) return left.length;

  const matrix = Array.from({ length: right.length + 1 }, (_, index) => [index]);
  for (let column = 0; column <= left.length; column += 1) {
    matrix[0][column] = column;
  }

  for (let row = 1; row <= right.length; row += 1) {
    for (let column = 1; column <= left.length; column += 1) {
      const cost = left[column - 1] === right[row - 1] ? 0 : 1;
      matrix[row][column] = Math.min(
        matrix[row - 1][column] + 1,
        matrix[row][column - 1] + 1,
        matrix[row - 1][column - 1] + cost,
      );
    }
  }

  return matrix[right.length][left.length];
}

function isCloseMatch(answer, guess) {
  const normalizedGuess = normalizeText(guess);
  const normalizedAnswer = normalizeText(answer);

  if (!normalizedGuess || normalizedGuess.length < 2) return false;
  if (normalizedGuess === normalizedAnswer) return true;
  if (normalizedAnswer.includes(normalizedGuess) || normalizedGuess.includes(normalizedAnswer)) {
    return true;
  }

  const distance = levenshtein(normalizedGuess, normalizedAnswer);
  const tolerance = Math.max(2, Math.floor(normalizedAnswer.length * 0.2));
  return distance <= tolerance;
}

function titleize(value) {
  return String(value)
    .split(/[-_\s]+/)
    .map((part) => part.charAt(0).toUpperCase() + part.slice(1))
    .join(' ');
}

function buildBoard(board) {
  const grouped = new Map();

  for (const category of CATEGORY_ORDER) {
    grouped.set(category, []);
  }

  for (const question of board?.questions ?? []) {
    const key = String(question.category ?? '').toLowerCase();
    if (!grouped.has(key)) {
      grouped.set(key, []);
    }
    grouped.get(key).push(question);
  }

  for (const [category, questions] of grouped.entries()) {
    questions.sort((left, right) => left.value - right.value);
    grouped.set(category, questions);
  }

  return Array.from(grouped.entries())
    .filter(([, questions]) => questions.length > 0)
    .map(([category, questions]) => ({
      category,
      questions,
    }));
}

function formatDuration(seconds) {
  const total = Math.max(0, Math.floor(seconds));
  const minutes = String(Math.floor(total / 60)).padStart(2, '0');
  const remaining = String(total % 60).padStart(2, '0');
  return `${minutes}:${remaining}`;
}

function App() {
  const [screen, setScreen] = useState('home');
  const [board, setBoard] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [selectedQuestion, setSelectedQuestion] = useState(null);
  const [guess, setGuess] = useState('');
  const [score, setScore] = useState(0);
  const [answered, setAnswered] = useState({});
  const [feedback, setFeedback] = useState(null);
  const [elapsed, setElapsed] = useState(0);
  const startTimeRef = useRef(0);
  const timerRef = useRef(null);

  const boardCode = board?.board_code;
  const boardGroups = useMemo(() => buildBoard(board), [board]);
  const answeredCount = Object.keys(answered).length;

  useEffect(() => {
    if (screen !== 'game' || !startTimeRef.current) return undefined;

    timerRef.current = window.setInterval(() => {
      setElapsed(Math.floor((Date.now() - startTimeRef.current) / 1000));
    }, 1000);

    return () => window.clearInterval(timerRef.current);
  }, [screen]);

  useEffect(() => {
    if (screen === 'game' && answeredCount === 25 && boardCode) {
      setFeedback({
        correct: true,
        reason: 'Board complete',
        message: 'You cleared the board.',
      });
    }
  }, [answeredCount, boardCode, screen]);

  async function startNewGame() {
    setLoading(true);
    setError('');

    try {
      const nextBoard = await createGameboard();
      setBoard(nextBoard);
      setAnswered({});
      setScore(0);
      setGuess('');
      setSelectedQuestion(null);
      setFeedback(null);
      setElapsed(0);
      startTimeRef.current = Date.now();
      setScreen('game');
    } catch (requestError) {
      setError(requestError.message || 'Unable to create a board right now.');
      setScreen('home');
    } finally {
      setLoading(false);
    }
  }

  function openQuestion(question) {
    const questionId = question.id ?? `${question.category}-${question.value}`;
    if (answered[questionId]) return;
    setSelectedQuestion(question);
    setGuess('');
    setFeedback(null);
  }

  function closeQuestion() {
    setSelectedQuestion(null);
    setGuess('');
  }

  function submitAnswer() {
    if (!selectedQuestion) return;

    const questionId = selectedQuestion.id ?? `${selectedQuestion.category}-${selectedQuestion.value}`;
    const correct = isCloseMatch(selectedQuestion.answer_text, guess);
    const updatedAnswered = { ...answered, [questionId]: true };

    setAnswered(updatedAnswered);
    setScore((currentScore) => currentScore + (correct ? selectedQuestion.value : 0));
    setFeedback({
      correct,
      reason: correct ? 'Accepted answer' : 'Incorrect',
      message: correct ? `+${selectedQuestion.value}` : `Correct answer: ${selectedQuestion.answer_text}`,
    });
    setSelectedQuestion(null);
    setGuess('');
  }

  if (screen === 'home') {
    return (
      <main className="app-shell app-shell--home">
        <section className="hero-panel">
          <p className="eyebrow">Grid Quiz</p>
          <h1>Turn the prototype into a real game.</h1>
          <p className="hero-copy">
            This frontend now creates boards from the Django API instead of relying on a static HTML demo.
          </p>
          <div className="hero-actions">
            <button className="primary-button" onClick={startNewGame} disabled={loading}>
              {loading ? 'Creating board...' : 'Start new board'}
            </button>
          </div>
          {error ? <p className="error-banner">{error}</p> : null}
        </section>

        <aside className="info-panel">
          <div className="info-card">
            <span className="info-label">Backend connection</span>
            <strong>GET /api/game/</strong>
            <p>The board is fetched from Django and rendered into React state.</p>
          </div>
          <div className="info-card">
            <span className="info-label">Current scope</span>
            <strong>Board creation and play loop</strong>
            <p>Leaderboard submission and auth wiring can be layered in next.</p>
          </div>
        </aside>
      </main>
    );
  }

  return (
    <main className="app-shell">
      <header className="topbar">
        <div>
          <p className="eyebrow">Grid Quiz</p>
          <h2>Board {boardCode}</h2>
        </div>
        <div className="topbar-stats">
          <span>Score ${score.toLocaleString()}</span>
          <span>Time {formatDuration(elapsed)}</span>
          <button className="ghost-button" onClick={() => setScreen('home')}>Home</button>
        </div>
      </header>

      <section className="board-panel">
        {boardGroups.map(({ category, questions }) => (
          <div key={category} className="category-column">
            <div className="category-header">{titleize(category)}</div>
            {VALUES.map((value) => {
              const question = questions.find((item) => item.value === value);
              const questionId = question?.id ?? `${category}-${value}`;
              const isUsed = Boolean(answered[questionId]);

              return (
                <button
                  key={questionId}
                  className={`question-tile ${isUsed ? 'question-tile--used' : ''}`}
                  onClick={() => question && openQuestion(question)}
                  disabled={!question || isUsed}
                >
                  ${value}
                </button>
              );
            })}
          </div>
        ))}
      </section>

      <footer className="status-bar">
        <span>{answeredCount}/25 answered</span>
        {feedback ? <span>{feedback.reason}: {feedback.message}</span> : <span>Select a tile to play.</span>}
      </footer>

      {selectedQuestion ? (
        <div className="modal-backdrop" role="presentation" onClick={closeQuestion}>
          <section className="question-modal" role="dialog" aria-modal="true" onClick={(event) => event.stopPropagation()}>
            <p className="eyebrow">{titleize(selectedQuestion.category)}</p>
            <h3>${selectedQuestion.value}</h3>
            <p className="clue-text">{selectedQuestion.question_text}</p>
            <label className="answer-label" htmlFor="guess-input">Your answer</label>
            <input
              id="guess-input"
              className="answer-input"
              value={guess}
              onChange={(event) => setGuess(event.target.value)}
              placeholder="Type your guess"
              autoComplete="off"
              autoFocus
            />
            <div className="modal-actions">
              <button className="ghost-button" onClick={closeQuestion}>Cancel</button>
              <button className="primary-button" onClick={submitAnswer}>Submit</button>
            </div>
          </section>
        </div>
      ) : null}
    </main>
  );
}

export default App;