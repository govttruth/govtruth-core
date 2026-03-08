-- GovTruth Database Schema
-- India Government Accountability Platform
-- All data sourced from official public records

-- MP Asset Declarations
-- Source: Election Commission of India
CREATE TABLE IF NOT EXISTS mp_assets (
    id SERIAL PRIMARY KEY,
    mp_name VARCHAR(200) NOT NULL,
    constituency VARCHAR(200),
    state VARCHAR(100),
    party VARCHAR(100),
    election_year INTEGER NOT NULL,
    total_assets BIGINT,
    total_liabilities BIGINT,
    movable_assets BIGINT,
    immovable_assets BIGINT,
    declared_income BIGINT,
    criminal_cases INTEGER DEFAULT 0,
    educational_qualification TEXT,
    source_url TEXT,
    source_document VARCHAR(100) DEFAULT 'ECI Official Affidavit',
    verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- CAG Audit Findings
-- Source: Comptroller & Auditor General of India
CREATE TABLE IF NOT EXISTS cag_findings (
    id SERIAL PRIMARY KEY,
    report_year INTEGER NOT NULL,
    report_number VARCHAR(50),
    ministry VARCHAR(200) NOT NULL,
    department VARCHAR(200),
    scheme VARCHAR(300),
    amount_crore DECIMAL(15,2),
    finding_type VARCHAR(100),
    -- Types: fraud, irregularity, 
    --        inefficiency, excess_payment,
    --        diversion, unspent
    finding_summary TEXT NOT NULL,
    paragraph_reference VARCHAR(50),
    followup_status VARCHAR(100) DEFAULT 'PENDING',
    parliament_discussed BOOLEAN DEFAULT FALSE,
    parliament_session VARCHAR(50),
    prosecution_initiated BOOLEAN DEFAULT FALSE,
    amount_recovered DECIMAL(15,2) DEFAULT 0,
    source_document TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Government Contracts
-- Source: Central Public Procurement Portal
CREATE TABLE IF NOT EXISTS contracts (
    id SERIAL PRIMARY KEY,
    tender_id VARCHAR(100) UNIQUE,
    ministry VARCHAR(200) NOT NULL,
    department VARCHAR(200),
    description TEXT,
    estimated_value BIGINT,
    awarded_value BIGINT,
    winner_company VARCHAR(300),
    winner_cin VARCHAR(50),
    bidder_count INTEGER,
    award_date DATE,
    completion_date DATE,
    actual_completion_date DATE,
    -- Flags
    political_connection_flag BOOLEAN DEFAULT FALSE,
    single_bidder_flag BOOLEAN DEFAULT FALSE,
    below_estimate_flag BOOLEAN DEFAULT FALSE,
    off_hours_award_flag BOOLEAN DEFAULT FALSE,
    satellite_verified VARCHAR(50) DEFAULT 'PENDING',
    risk_score INTEGER DEFAULT 0,
    source TEXT DEFAULT 'CPP Portal - eprocure.gov.in',
    created_at TIMESTAMP DEFAULT NOW()
);

-- Electoral Bond Transactions
-- Source: SBI Disclosure (Supreme Court Order)
CREATE TABLE IF NOT EXISTS electoral_bonds (
    id SERIAL PRIMARY KEY,
    bond_number VARCHAR(100),
    purchaser_company VARCHAR(300) NOT NULL,
    purchaser_cin VARCHAR(50),
    purchase_date DATE NOT NULL,
    amount BIGINT NOT NULL,
    encashment_date DATE,
    party_received VARCHAR(200),
    -- Post-purchase analysis
    govt_contracts_won_after BIGINT DEFAULT 0,
    days_to_first_contract INTEGER,
    suspicious_timeline BOOLEAN DEFAULT FALSE,
    political_connection_verified BOOLEAN DEFAULT FALSE,
    source TEXT DEFAULT 
        'SBI Disclosure + ECI Party Accounts',
    created_at TIMESTAMP DEFAULT NOW()
);

-- Satellite Verifications
-- Source: ESA Sentinel-2 / Google Earth Engine
CREATE TABLE IF NOT EXISTS satellite_verifications (
    id SERIAL PRIMARY KEY,
    project_id VARCHAR(100),
    project_name TEXT NOT NULL,
    ministry VARCHAR(200),
    claimed_cost_crore DECIMAL(15,2),
    claimed_completion DATE,
    coordinates_lat DECIMAL(10,6) NOT NULL,
    coordinates_lon DECIMAL(10,6) NOT NULL,
    -- Results
    verification_result VARCHAR(50),
    -- CONFIRMED / PARTIAL / UNVERIFIED / CONTRADICTED
    confidence_score DECIMAL(5,2),
    before_image_date DATE,
    after_image_date DATE,
    change_detected BOOLEAN,
    change_magnitude DECIMAL(5,2),
    analyst_notes TEXT,
    satellite_source VARCHAR(100) 
        DEFAULT 'ESA Sentinel-2',
    created_at TIMESTAMP DEFAULT NOW()
);

-- Politician Profiles
-- Aggregated from ECI + MCA21 + Court Records
CREATE TABLE IF NOT EXISTS politicians (
    id SERIAL PRIMARY KEY,
    full_name VARCHAR(200) NOT NULL,
    aliases TEXT[],
    current_position VARCHAR(200),
    party VARCHAR(100),
    constituency VARCHAR(200),
    state VARCHAR(100),
    -- ECI data
    eci_candidate_id VARCHAR(50),
    first_election_year INTEGER,
    total_terms INTEGER DEFAULT 0,
    -- Asset summary (from latest affidavit)
    latest_declared_assets BIGINT,
    asset_growth_percent DECIMAL(8,2),
    unexplained_growth BIGINT,
    risk_score INTEGER DEFAULT 0,
    -- Criminal record
    total_criminal_cases INTEGER DEFAULT 0,
    serious_cases INTEGER DEFAULT 0,
    -- Business connections
    company_directorships INTEGER DEFAULT 0,
    family_company_connections INTEGER DEFAULT 0,
    govt_contracts_connected BIGINT DEFAULT 0,
    -- Flags
    offshore_leak_mention BOOLEAN DEFAULT FALSE,
    cag_finding_connected BOOLEAN DEFAULT FALSE,
    electoral_bond_connected BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Citizen Reports
-- Anonymous submissions from verified citizens
CREATE TABLE IF NOT EXISTS citizen_reports (
    id SERIAL PRIMARY KEY,
    report_hash VARCHAR(64) UNIQUE NOT NULL,
    category VARCHAR(100) NOT NULL,
    district VARCHAR(100),
    state VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    evidence_urls TEXT[],
    gps_lat DECIMAL(10,6),
    gps_lon DECIMAL(10,6),
    -- Verification
    verification_status VARCHAR(50) 
        DEFAULT 'PENDING',
    verified_by_satellite BOOLEAN DEFAULT FALSE,
    verified_by_reporter_count INTEGER DEFAULT 1,
    reporter_reputation_score DECIMAL(3,2),
    -- Escalation
    escalated_to_journalist BOOLEAN DEFAULT FALSE,
    escalated_to_rti BOOLEAN DEFAULT FALSE,
    outcome TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Indexes for performance
CREATE INDEX idx_mp_assets_name 
    ON mp_assets(mp_name);
CREATE INDEX idx_mp_assets_year 
    ON mp_assets(election_year);
CREATE INDEX idx_mp_assets_party 
    ON mp_assets(party);
CREATE INDEX idx_cag_ministry 
    ON cag_findings(ministry);
CREATE INDEX idx_cag_year 
    ON cag_findings(report_year);
CREATE INDEX idx_contracts_ministry 
    ON contracts(ministry);
CREATE INDEX idx_contracts_winner 
    ON contracts(winner_company);
CREATE INDEX idx_bonds_company 
    ON electoral_bonds(purchaser_company);
CREATE INDEX idx_bonds_party 
    ON electoral_bonds(party_received);
CREATE INDEX idx_politicians_name 
    ON politicians(full_name);
CREATE INDEX idx_politicians_party 
    ON politicians(party);

-- Comments for documentation
COMMENT ON TABLE mp_assets IS 
    'MP asset declarations from ECI affidavits. 
     Source: affidavitarchive.nic.in';
     
COMMENT ON TABLE cag_findings IS 
    'Audit findings from CAG reports. 
     Source: cag.gov.in/en/audit-report';
     
COMMENT ON TABLE contracts IS 
    'Government contracts from CPP portal. 
     Source: eprocure.gov.in';
     
COMMENT ON TABLE electoral_bonds IS 
    'Electoral bond data from SBI disclosure. 
     Source: Supreme Court ordered disclosure 2024';
