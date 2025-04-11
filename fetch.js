// Company object with type annotations
const company: {
    code: string;              // char (unique)
    title: string;             // char (unique)
    industry: string;          // char (classification)
    vertical: string;          // char (classification)
    canton: string;            // char (classification)
    spinOffs: string[];        // list
    city: string;              // char
    year: number;              // int
    highlights: string[];      // list
    genderCEO: string;         // char (classification)
    oob: boolean;              // bool
    funded: boolean;           // bool
    comment: string;           // char
  };
  
  // Deal object with type annotations
  const deal: {
    id: string;                // char (unique generated)
    investors: string;         // char
    amount: number;            // numeric
    valuation: number;         // numeric
    comment: string;           // char
    url: string;               // char
    confidential: boolean;     // bool
    amountConfidential: boolean; // bool
    dateOfFundingRound: Date;  // date
    type: string;              // char (classification)
    phase: string;             // char (classification)
    canton: string;            // char (classification)
    company: string;           // char (reference to Company.code)
    genderCEO: string;         // char (classification)
  };