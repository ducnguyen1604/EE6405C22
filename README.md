# EE6405C22

Repo for NLP EE 6405 group C22

## A. Run the Frontend (Next.js)

```bash
cd frontend
npm run dev
```

The UI is hosted at: [http://localhost:3000](http://localhost:3000)

---

## B. Run the Backend (FastAPI)

1. Create and activate a Python virtual environment

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Start the backend server:

```bash
uvicorn main:app --reload
```

The backend is hosted at: [http://localhost:8000](http://localhost:8000)

---

## C. API Endpoints

### 1. GET `/search`

#### Query Parameters:
- `q` (string): Search query (e.g., `REMOVED_SECRETbreadREMOVED_SECRET`)
- `langs` (string, optional): Comma-separated list of languages, e.g., `REMOVED_SECRETChinese,SpanishREMOVED_SECRET`

#### Example:

```http
GET /search?q=mouth spray&langs=Chinese,Spanish,Italian
```

#### Sample Response:

```json
{
  REMOVED_SECRETtranslationsREMOVED_SECRET: {
    REMOVED_SECRETChineseREMOVED_SECRET: REMOVED_SECRET口腔喷雾REMOVED_SECRET,
    REMOVED_SECRETSpanishREMOVED_SECRET: REMOVED_SECRETspray oralREMOVED_SECRET,
    REMOVED_SECRETItalianREMOVED_SECRET: REMOVED_SECRETspray oraleREMOVED_SECRET
  },
  REMOVED_SECRETproductsREMOVED_SECRET: [
    {
      REMOVED_SECRETidREMOVED_SECRET: 1,
      REMOVED_SECRETnameREMOVED_SECRET: {
        REMOVED_SECRETenREMOVED_SECRET: REMOVED_SECRETMouth SprayREMOVED_SECRET,
        REMOVED_SECRETzhREMOVED_SECRET: REMOVED_SECRET口腔喷雾REMOVED_SECRET
      },
      REMOVED_SECRETdescriptionREMOVED_SECRET: {
        REMOVED_SECRETenREMOVED_SECRET: REMOVED_SECRETFreshens breathREMOVED_SECRET
      }
    }
  ]
}
```

---

### 2. GET `/product/{id}`

#### Path Parameter:
- `id` (int): Product ID (e.g., `1`)

#### Example:

```http
GET /product/1
```

Returns the product details, or a 404 if not found.
