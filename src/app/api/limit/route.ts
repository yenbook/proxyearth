import { NextRequest, NextResponse } from 'next/server';
import { getDb } from '@/lib/db';

export const runtime = 'edge';

export async function GET(request: NextRequest) {
    try {
        const pool = getDb();

        // Ensure table exists (just in case)
        await pool.query(`
            CREATE TABLE IF NOT EXISTS daily_usage (
                ip VARCHAR(45),
                date DATE DEFAULT CURRENT_DATE,
                count INTEGER DEFAULT 0,
                PRIMARY KEY (ip, date)
            );
        `);

        const clientIp = request.headers.get('cf-connecting-ip') || request.headers.get('x-forwarded-for') || '127.0.0.1';

        const result = await pool.query(`
            SELECT count FROM daily_usage 
            WHERE ip = $1 AND date = CURRENT_DATE
        `, [clientIp]);

        const count = result.rows.length > 0 ? result.rows[0].count : 0;
        const limit = 30;

        return NextResponse.json({
            count,
            limit,
            remaining: Math.max(0, limit - count)
        });

    } catch (error) {
        console.error("Limit Check Error:", error);
        return NextResponse.json({ count: 0, limit: 30, remaining: 30 }, { status: 200 }); // Fail gracefully
    }
}
