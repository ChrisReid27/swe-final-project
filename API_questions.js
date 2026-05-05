/**
 * Grid Quiz API Question Generator
 * Fetches real-time data to populate the trivia board.
 */

const API_KEYS = {
  OMDB: 'YOUR_OMDB_KEY',
  SPOTIFY_CLIENT_ID: 'YOUR_ID',
  SPOTIFY_SECRET: 'YOUR_SECRET'
};

const generateDynamicQuestions = async () => {
  const newQuestions = {
    Movies: [],
    Music: [],
    Sports: [],
    TV: [], // You can add TMDB API for this
    Celebrities: []
  };

  try {
    // --- 1. POPULATE MOVIES (OMDb) ---
    // We fetch 5 popular movies and turn them into clues
    const movieTitles = ['Inception', 'Parasite', 'The Matrix', 'Gladiator', 'Interstellar'];
    for (let i = 0; i < movieTitles.length; i++) {
      const res = await fetch(`https://www.omdbapi.com/?t=${movieTitles[i]}&apikey=${API_KEYS.OMDB}`);
      const data = await res.json();
      
      newQuestions.Movies.push({
        value: (i + 1) * 200,
        clue: `This ${data.Year} film directed by ${data.Director} stars ${data.Actors.split(',')[0]}.`,
        answer: data.Title,
        hint: `Plot: ${data.Plot.substring(0, 50)}...`,
        howard: false
      });
    }

    // --- 2. POPULATE MUSIC (Spotify) ---
    // Note: Spotify requires an Auth Token. This is a simplified fetch logic.
    const spotifySongs = ['Blinding Lights', 'vampire', 'Flowers', 'Humble', 'Anti-Hero'];
    spotifySongs.forEach((song, i) => {
       newQuestions.Music.push({
         value: (i + 1) * 200,
         clue: `This hit track by a famous artist features the lyrics/theme of "${song}".`,
         answer: song,
         hint: "It was a chart-topping single on Spotify.",
         howard: i === 1 // Randomly assign a 'Howard' special tile
       });
    });

    // --- 3. POPULATE SPORTS (Example using a Mock/Static Mix for ESPN style) ---
    const sportsData = [
      { a: "Lakers", c: "This NBA team plays at the Crypto.com Arena and features purple and gold colors." },
      { a: "Super Bowl", c: "This annual championship game is the culmination of the NFL season." },
      { a: "Lionel Messi", c: "This Argentinian legend led his country to World Cup glory in 2022." },
      { a: "Wimbledon", c: "This is the oldest tennis tournament in the world, played on grass." },
      { a: "Tiger Woods", c: "This golfer has won 15 professional major golf championships." }
    ];
    
    sportsData.forEach((item, i) => {
      newQuestions.Sports.push({
        value: (i + 1) * 200,
        clue: item.c,
        answer: item.a,
        hint: "Think of the biggest names in the game.",
        howard: false
      });
    });

    return newQuestions;

  } catch (error) {
    console.error("Error fetching API data, falling back to static questions", error);
    return null; // Fallback to your hardcoded QUESTIONS
  }
};


// In html: change const [questions, setQuestions] = useState(QUESTIONS); inside main App component.
// AND add:
/*
useEffect(() => {
  const loadQuestions = async () => {
    const apiQuestions = await generateDynamicQuestions();
    if (apiQuestions) {
      setQuestions(apiQuestions);
    }
  };
  loadQuestions();
}, []);
*/
