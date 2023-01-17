import { createSignal } from 'solid-js';

function App() {
  const [yearsExperience, setYearsExperience] = createSignal('');
  const [prediction, setPrediction] = createSignal('');

  const handlerSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch('http://localhost:8000/predict_api', {
        method: 'POST',
        body: JSON.stringify({ year: yearsExperience() }),
        headers: { 'Content-Type': 'application/json' },
      });
      const data = await response.json();
      setPrediction(data.output);
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div class="flex justify-center">
      <div class="bg-white p-10 rounded-lg shadow-md">
        <h3 className="text-muted text-center py-2">
          Salary prediction Based on Experience
        </h3>

        <form onSubmit={handlerSubmit}>
          <div class="relative rounded-md shadow-sm">
            <input
              class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5"
              type="text"
              name="YearsExperience"
              placeholder="Years of Experience"
              required
              onChange={(e) => setYearsExperience(e.target.value)}
            />
          </div>
          <button
            class="mt-6 bg-blue-500 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded-md"
            type="submit"
          >
            Predict
          </button>
        </form>
        <br />
        <br />
        {prediction() && <p>Prediction: {prediction()}</p>}
      </div>
    </div>
  );
}

export default App;
