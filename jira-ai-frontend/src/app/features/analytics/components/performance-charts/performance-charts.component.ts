import { Component, Input, OnInit, OnChanges, SimpleChanges } from '@angular/core';
import { CommonModule } from '@angular/common';
import { BaseChartDirective } from 'ng2-charts';
import { ChartConfiguration, ChartData } from 'chart.js';
import { PerformanceMetrics } from '../../../../core/models/analytics.model';

@Component({
  selector: 'app-performance-charts',
  standalone: true,
  imports: [CommonModule, BaseChartDirective],
  templateUrl: './performance-charts.component.html',
  styleUrls: ['./performance-charts.component.scss']
})
export class PerformanceChartsComponent implements OnInit, OnChanges {
  @Input() metrics!: PerformanceMetrics;

  // Velocity Chart
  velocityChartData: ChartData<'bar'> = { labels: [], datasets: [] };
  velocityChartOptions: ChartConfiguration<'bar'>['options'] = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: { display: true, position: 'bottom' }
    },
    scales: {
      y: { beginAtZero: true, grid: { color: '#EBECF0' } },
      x: { grid: { display: false } }
    }
  };

  // Cycle Time Chart
  cycleTimeChartData: ChartData<'line'> = { labels: [], datasets: [] };
  cycleTimeChartOptions: ChartConfiguration<'line'>['options'] = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: { display: false }
    },
    scales: {
      y: { 
        beginAtZero: false, 
        grid: { color: '#EBECF0' },
        ticks: { callback: (value) => value + ' days' }
      },
      x: { grid: { display: false } }
    },
    elements: {
      line: { tension: 0.4 },
      point: { radius: 4, hoverRadius: 6 }
    }
  };

  // Throughput Chart
  throughputChartData: ChartData<'line'> = { labels: [], datasets: [] };
  throughputChartOptions: ChartConfiguration<'line'>['options'] = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: { display: false }
    },
    scales: {
      y: { beginAtZero: true, grid: { color: '#EBECF0' } },
      x: { grid: { display: false } }
    },
    elements: {
      line: { tension: 0.4 },
      point: { radius: 4, hoverRadius: 6 }
    }
  };

  ngOnInit(): void {
    this.updateCharts();
  }

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['metrics']) {
      this.updateCharts();
    }
  }

  private updateCharts(): void {
    if (!this.metrics) return;

    // Velocity Chart
    this.velocityChartData = {
      labels: this.metrics.velocityTrend.map(v => v.sprint),
      datasets: [
        {
          label: 'Planned',
          data: this.metrics.velocityTrend.map(v => v.planned),
          backgroundColor: 'rgba(0, 82, 204, 0.7)'
        },
        {
          label: 'Completed',
          data: this.metrics.velocityTrend.map(v => v.completed),
          backgroundColor: 'rgba(54, 179, 126, 0.7)'
        }
      ]
    };

    // Cycle Time Chart
    this.cycleTimeChartData = {
      labels: this.metrics.cycleTimeTrend.map(c => c.week),
      datasets: [
        {
          label: 'Cycle Time',
          data: this.metrics.cycleTimeTrend.map(c => c.averageDays),
          borderColor: '#FFAB00',
          backgroundColor: 'rgba(255, 171, 0, 0.1)',
          fill: true
        }
      ]
    };

    // Throughput Chart
    this.throughputChartData = {
      labels: this.metrics.throughputTrend.map(t => t.week),
      datasets: [
        {
          label: 'Throughput',
          data: this.metrics.throughputTrend.map(t => t.count),
          borderColor: '#6554C0',
          backgroundColor: 'rgba(101, 84, 192, 0.1)',
          fill: true
        }
      ]
    };
  }

  // Calculate summary metrics
  get averageVelocity(): number {
    const completed = this.metrics.velocityTrend.map(v => v.completed);
    return completed.reduce((a, b) => a + b, 0) / completed.length;
  }

  get velocityTrend(): string {
    const trend = this.metrics.velocityTrend;
    const recent = trend.slice(-3).map(v => v.completed);
    const older = trend.slice(0, 3).map(v => v.completed);
    const recentAvg = recent.reduce((a, b) => a + b, 0) / recent.length;
    const olderAvg = older.reduce((a, b) => a + b, 0) / older.length;
    return recentAvg > olderAvg ? 'improving' : 'declining';
  }

  get averageCycleTime(): number {
    const times = this.metrics.cycleTimeTrend.map(c => c.averageDays);
    return times.reduce((a, b) => a + b, 0) / times.length;
  }

  get totalThroughput(): number {
    return this.metrics.throughputTrend.reduce((sum, t) => sum + t.count, 0);
  }
}