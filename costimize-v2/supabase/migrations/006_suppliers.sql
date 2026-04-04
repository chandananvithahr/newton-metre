-- Supplier registry for procurement workflows.

CREATE TABLE IF NOT EXISTS suppliers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    company_id UUID NOT NULL,
    name TEXT NOT NULL,
    email TEXT,
    phone TEXT,
    categories TEXT[] DEFAULT '{}',       -- part categories this supplier handles
    regions TEXT[] DEFAULT '{}',          -- geographic regions
    rating DECIMAL(3, 2) DEFAULT 0,      -- 0-5 supplier rating
    preferred BOOLEAN DEFAULT false,
    notes TEXT DEFAULT '',
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_suppliers_company ON suppliers(company_id);
CREATE INDEX idx_suppliers_categories ON suppliers USING GIN(categories);

ALTER TABLE suppliers ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Company isolation on suppliers"
    ON suppliers FOR ALL
    USING (company_id::text = auth.uid()::text OR auth.role() = 'service_role');

-- Supplier contacts
CREATE TABLE IF NOT EXISTS supplier_contacts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    supplier_id UUID NOT NULL REFERENCES suppliers(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    email TEXT,
    role TEXT DEFAULT '',
    is_primary BOOLEAN DEFAULT false,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE INDEX idx_supplier_contacts_supplier ON supplier_contacts(supplier_id);

ALTER TABLE supplier_contacts ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Service role full access on contacts"
    ON supplier_contacts FOR ALL
    USING (auth.role() = 'service_role');
