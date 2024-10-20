import { useEffect, useState } from 'react';
import './App.css';
import { Box, Button, ButtonGroup, FormControl, FormControlLabel, FormHelperText, FormLabel, InputLabel, MenuItem, Radio, RadioGroup, Select, Stack, TextField } from '@mui/material';

function App() {
  const [rule, setRule] = useState<string>('');
  const [rule1, setRule1] = useState<string>('');
  const [rule2, setRule2] = useState<string>('');
  const [ruleError, setRuleError] = useState<string>('');
  const [view, setView] = useState<string>('Create');
  const [genereateAST, setGeneratedAST] = useState('');
  const [generatedCombinedAST, setGeneratedCombinedAST] = useState('');
  const [operator, setOperator] = useState<string>('AND');
  const [fetchedRules, setFetchedRules] = useState<[]>([]);
  const handleOperatorChange = (operator: string) => {
    setOperator(operator);
  }
  const handleCreateRuleClick = async () => {
    const response = await fetch('http://127.0.0.1:8000/api/rules/save', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ rule })
    });
    const data = await response.json();
    if (response.ok) {
      setGeneratedAST(data.ast);
    }
  }
  const handleCombineRuleClick = async () => {
    const response = await fetch('http://127.0.0.1:8000/api/rules/combine', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        rules: [rule1, rule2],
        combine_operator: operator
      })

    });

    const data = await response.json();
    if (response.ok) {
      setGeneratedCombinedAST(data.ast);
    }
  }
  useEffect(() => {
    // You can add any side-effects here if needed
    async function fetchRules() {
      const response = await fetch('http://127.0.0.1:8000/api/rules/get-rules', {
        method: 'GET'
      });
      const data = await response.json();
      if (response.ok) {
        setFetchedRules(data.rules);
        console.log(fetchedRules);
      }
    }
    fetchRules();
    console.log(fetchedRules);
  }, []);
  useEffect(() => {
    console.log('Updated fetchedRules:', fetchedRules);
  }, [fetchedRules]);  // This runs every time `fetchedRules` changes

  const handleRuleChange = (event: any) => {
    setRule(event.target.value);
    setGeneratedAST("");
  };
  const handleRule1Change = (event: any) => {
    setRule1(event.target.value);
    setGeneratedAST("");
  };
  const handleRule2Change = (event: any) => {
    setRule2(event.target.value);
    setGeneratedAST("");
  };

  const handleShowClick = (view: string) => {
    setView(view);
  };

  const [evaluateRule, setEvaluateRule] = useState<string>('');
  const handleEvaluateRuleChange = (event: any) => {
    setEvaluateRule(event.target.value);
    setGeneratedAST("");
  };

  const [jsonData, setJsonData] = useState<string>('');
  const handleJsonChange = (event: any) => {
    setJsonData(event.target.value);
  }
  const handleEvaluateRuleClick = async () => {
    // alert(jsonData);
    console.log(evaluateRule);
    console.log(jsonData);
    const response = await fetch('http://127.0.0.1:8000/api/rules/evaluate', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        rule: evaluateRule,
        data: jsonData
      })
    });
    const data = await response.json();

    if (data.result) {
      alert("The rule passed for the given data");
    }
    else {
      alert("The rule failed for the given data");
    }
  }

  const [isRuleSelected, setIsRuleSelected] = useState<boolean>(false);
  const handleRuleSelectClick = (rule: string) => {
    setRule(rule);
    setIsRuleSelected(true);
  }
  return (
    <div className='d-flex flex-column gap-3'>
      <Box display="flex" justifyContent="center" marginBottom={2}>
        <ButtonGroup>
          <Button
            onClick={() => handleShowClick('Create')}
            variant={view === "Create" ? "contained" : "outlined"}
          >
            Create / Modify Rule
          </Button>
          <Button
            onClick={() => handleShowClick('Combine')}
            variant={view === "Combine" ? "contained" : "outlined"}
          >
            Combine Rules
          </Button>
          <Button
            onClick={() => handleShowClick('Evaluate')}
            variant={view === "Evaluate" ? "contained" : "outlined"}
          >
            Evaluate
          </Button>
        </ButtonGroup>
      </Box>

      <div>
        {/* Create Rule section */}
        {
          view === 'Create' &&
          <div className='d-flex flex-column gap-2'>
            <FormControl fullWidth>
              <InputLabel id="demo-simple-select-label">Select rule to edit</InputLabel>
              <Select label="Select rule to edit" autoWidth>
                {fetchedRules.length > 0 ? (
                  fetchedRules.map((rule, index) => (
                    <MenuItem key={index} value={rule} onClick={() => handleRuleSelectClick(rule)}>
                      {rule}
                    </MenuItem>
                  ))
                ) : (
                  <MenuItem disabled>No rules available</MenuItem>
                )}
              </Select>
            </FormControl>

            <TextField
              label={isRuleSelected ? "Edit Selected Rule" : "Create Rule"}
              variant="outlined"
              onChange={handleRuleChange}
              value={rule}
              error={Boolean(ruleError)}
              fullWidth
            />
            <p className="text-danger">
              {ruleError}
            </p>
            <Button variant="contained" color="primary" onClick={handleCreateRuleClick}>
              Create Rule
            </Button>
            <div>
              <h4>Generated AST</h4>
              <TextField
                multiline
                contentEditable="false"
                value={genereateAST}
                fullWidth
              />
              {/* {genereateAST} */}
            </div>
          </div>
        }

        {/* Combine rules section */}
        {view === 'Combine' &&
          <div className='d-flex flex-column gap-3'>
            <div className='d-flex flex-column gap-2'>
              {/* Your combine rules content goes here */}
              <Stack spacing={2}>
                <TextField
                  label="Rule 1"
                  variant="outlined"
                  onChange={handleRule1Change}
                  value={rule1}
                  error={Boolean(ruleError)}
                  fullWidth
                />
                <TextField
                  label="Rule 2"
                  variant="outlined"
                  onChange={handleRule2Change}
                  value={rule2}
                  error={Boolean(ruleError)}
                  fullWidth
                />
              </Stack>
              <FormControl className='d-flex justify-content-center align-items-center'>
                <FormLabel id="demo-row-radio-buttons-group-label">Choose Operator</FormLabel>
                <RadioGroup
                  row
                  aria-labelledby="demo-row-radio-buttons-group-label"
                  value={operator}
                  name="row-radio-buttons-group"
                  defaultValue="AND"
                >
                  <FormControlLabel value="AND" control={<Radio onChange={(e) => handleOperatorChange(e.target.value)} />} label="AND" />
                  <FormControlLabel value="OR" control={<Radio onChange={(e) => handleOperatorChange(e.target.value)} />} label="OR" />
                </RadioGroup>
              </FormControl>
              <Button variant="contained" color="primary" onClick={handleCombineRuleClick}>
                Combine Rules
              </Button>
            </div>
            <div>
              <h4>Generated AST</h4>
              <TextField
                multiline
                contentEditable="false"
                value={generatedCombinedAST}
                fullWidth
              />
              {/* {genereateAST} */}
            </div>
          </div>
        }

        {/* Evaluate rule section */}
        {view === 'Evaluate' &&
          <div>
            <div className='d-flex flex-column gap-2'>
              {/* Your evaluate rule content goes here */}
              <TextField
                label="Evaluate Rule"
                variant="outlined"
                onChange={handleEvaluateRuleChange}
                fullWidth
              />
              <TextField
                label="Data"
                multiline
                variant="outlined"
                onChange={handleJsonChange}
                fullWidth
              />
              <Button variant="contained" color="primary" onClick={handleEvaluateRuleClick}>
                Evaluate Rule
              </Button>
            </div>
          </div>
        }
      </div>
    </div>
  );
}

export default App;
